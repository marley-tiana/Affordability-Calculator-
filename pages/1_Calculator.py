import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="NOLA Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# New Orleans average utilities + internet estimates (monthly)
# Sources: Expat Arrivals (expatarrivals.com), ApartmentList, Entergy New Orleans
# Basic utilities (electricity, water, gas): ~$207/mo for 915 sq ft (Expat Arrivals)
# Internet: ~$65/month (Expat Arrivals)
UTILITIES_AVG = {
    "studio": 230,   # ~$165 utilities + $65 internet
    "1bed": 272,     # ~$207 utilities + $65 internet
    "2bed": 313,     # ~$248 utilities + $65 internet
    "3bed": 354,     # ~$289 utilities + $65 internet
    "4bed": 395,     # ~$330 utilities + $65 internet
}

WIFI_SETUP_FEE = 100  # router/modem setup fee (one-time)

# transportation costs
# Source: RTA New Orleans, Expat Arrivals
BUS_FARE_PER_RIDE = 1.25  # official RTA rate (free transfers)
JAZZY_PASS_MONTHLY = 45   # 31-day unlimited pass (RTA)
UBER_AVG_COST = 15        # average ride in New Orleans
DAYS_IN_PERIOD = 60

# session state — keeps inputs and results across reruns
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "calculation_results" not in st.session_state:
    st.session_state.calculation_results = None
if "show_results" not in st.session_state:
    st.session_state.show_results = False

# restore inputs from the backup dict if we're returning from another page
# (widget keys can get dropped during st.switch_page navigation in some Streamlit versions,
# but a plain dict in session state survives more reliably)
_saved = st.session_state.get("_calc_form", {})

if "calc_rent" not in st.session_state:
    st.session_state.calc_rent = _saved.get("calc_rent", 0.0)
if "calc_deposit" not in st.session_state:
    st.session_state.calc_deposit = _saved.get("calc_deposit", 0.0)
if "calc_application" not in st.session_state:
    st.session_state.calc_application = _saved.get("calc_application", 0.0)
if "calc_admin" not in st.session_state:
    st.session_state.calc_admin = _saved.get("calc_admin", 0.0)
if "calc_house_type" not in st.session_state:
    st.session_state.calc_house_type = _saved.get("calc_house_type", "studio")
if "calc_roommates" not in st.session_state:
    st.session_state.calc_roommates = _saved.get("calc_roommates", 0)
if "calc_transport_mode" not in st.session_state:
    st.session_state.calc_transport_mode = _saved.get("calc_transport_mode", "School shuttle (free)")
if "calc_savings" not in st.session_state:
    st.session_state.calc_savings = _saved.get("calc_savings", 0.0)
if "calc_uber_cost" not in st.session_state:
    st.session_state.calc_uber_cost = _saved.get("calc_uber_cost", float(UBER_AVG_COST))
if "calc_bus_rides" not in st.session_state:
    st.session_state.calc_bus_rides = _saved.get("calc_bus_rides", 2)
if "calc_uber_rides" not in st.session_state:
    st.session_state.calc_uber_rides = _saved.get("calc_uber_rides", 1)


def _save_form():
    """Save all input values to a backup dict whenever any field changes."""
    st.session_state["_calc_form"] = {
        "calc_rent": st.session_state.get("calc_rent", 0.0),
        "calc_deposit": st.session_state.get("calc_deposit", 0.0),
        "calc_application": st.session_state.get("calc_application", 0.0),
        "calc_admin": st.session_state.get("calc_admin", 0.0),
        "calc_house_type": st.session_state.get("calc_house_type", "studio"),
        "calc_roommates": st.session_state.get("calc_roommates", 0),
        "calc_transport_mode": st.session_state.get("calc_transport_mode", "School shuttle (free)"),
        "calc_savings": st.session_state.get("calc_savings", 0.0),
        "calc_uber_cost": st.session_state.get("calc_uber_cost", float(UBER_AVG_COST)),
        "calc_bus_rides": st.session_state.get("calc_bus_rides", 2),
        "calc_uber_rides": st.session_state.get("calc_uber_rides", 1),
    }


def validate_inputs(rent, deposit, application, admin, savings):
    """Validate user inputs before calculation."""
    errors = []
    if rent <= 0:
        errors.append("💰 **Monthly Rent** is required and must be greater than $0")
    if savings < 0:
        errors.append("💵 **Savings** cannot be negative")
    if rent > 10000:
        errors.append("💰 **Monthly Rent** seems unusually high. Please verify.")
    if deposit > rent * 3:
        errors.append("🔐 **Security Deposit** seems unusually high (typically 1-2 months rent)")
    total_input = rent + deposit + application + admin + savings
    if total_input == 0:
        errors.append("⚠️ Please enter at least your **Monthly Rent** and **Savings** to calculate")
    return len(errors) == 0, errors


def calculate_transport_cost(mode, rides_per_day=0, uber_cost=UBER_AVG_COST):
    """Calculate total transportation cost for 60-day period."""
    if mode in ("School shuttle (free)", "Walking", "Bike"):
        return 0
    elif mode == "Public transport (bus/train)":
        return BUS_FARE_PER_RIDE * rides_per_day * DAYS_IN_PERIOD
    elif mode == "Uber / Lyft":
        return uber_cost * rides_per_day * DAYS_IN_PERIOD

    return 0


def calculate_affordability(rent, deposit, application, admin, unit_type,
                            roommates, transport, savings):
    """Calculate housing affordability for first 60 days."""
    if roommates < 0:
        roommates = 0
    split_factor = 1 + roommates
    utilities = UTILITIES_AVG.get(unit_type, UTILITIES_AVG["1bed"])

    day0_cost = (deposit + rent + admin + utilities + WIFI_SETUP_FEE) / split_factor + application
    day60_cost = day0_cost + (rent + utilities) / split_factor + transport
    remaining_balance = savings - day60_cost

    breakdown = {
        "Rent (2 months)": (2 * rent) / split_factor,
        "Utilities & WiFi": (2 * utilities + WIFI_SETUP_FEE) / split_factor,
        "Transportation": transport,
        "One-Time Move-In Costs": (deposit + admin) / split_factor + application,
    }
    return day0_cost, day60_cost, remaining_balance, breakdown


def get_risk_level(remaining, day60_cost):
    """Determine financial risk level based on remaining balance."""
    if remaining < 0:
        return "high", "🔴"
    elif remaining < 0.1 * day60_cost:
        return "medium", "🟡"
    elif remaining < 0.2 * day60_cost:
        return "low", "🟠"
    else:
        return "none", "🟢"


st.title("🧮 Arrival Shock Calculator")
st.markdown("**First 60-Day Housing Costs for Students in New Orleans**")

st.info(
    "💡 This tool estimates your early-stage housing costs to help you understand "
    "the financial commitment of moving to New Orleans."
)

st.divider()

with st.expander("📚 Need help? View Housing Cost Definitions", expanded=False):
    st.markdown(
        "**Monthly Rent** - The money you pay every month. "
        "*Enter the total rent before dividing with roommates.*\n\n"
        "**Security Deposit** - A refundable payment made before moving in. "
        "Usually equal to one month's rent.\n\n"
        "**Application Fee** - A non-refundable fee for applying. "
        "Covers background checks.\n\n"
        "**Administrative Fee** - A non-refundable fee for lease preparation.\n\n"
        "**Utilities + Internet** - Monthly costs for electricity, water, gas, and internet (~$65/mo). "
        "Based on New Orleans averages from Expat Arrivals & Entergy New Orleans.\n\n"
        f"**Wi-Fi Setup** - One-time router/modem setup cost (${WIFI_SETUP_FEE}).\n\n"
        "**Roommates** - Shared housing costs are divided evenly. "
        "Transportation costs remain individual.\n\n"
        "💵 *All amounts in U.S. dollars ($).* | "
        "*Data sources: [RentCafe](https://www.rentcafe.com/average-rent-market-trends/us/la/new-orleans/), "
        "[Expat Arrivals](https://www.expatarrivals.com/americas/usa/new-orleans/cost-living-new-orleans), "
        "[RTA/Token Transit](https://tokentransit.com/agency/neworleansrta), "
        "Entergy New Orleans*\n\n"
        "---\n\n"
        "For more detailed explanations, budgeting strategies, and examples, "
        "visit our **Help** page."
    )

st.divider()

st.header("🏘️ Housing Costs")

col1, col2 = st.columns(2)
with col1:
    rent = st.number_input(
        "💰 Monthly Rent ($)", min_value=0.0, step=50.0,
        key="calc_rent", on_change=_save_form,
        help="Enter total rent before dividing with roommates."
    )
with col2:
    deposit = st.number_input(
        "🔐 Security Deposit ($)", min_value=0.0, step=50.0,
        key="calc_deposit", on_change=_save_form,
        help="A refundable payment made before moving in."
    )

col3, col4 = st.columns(2)
with col3:
    application = st.number_input(
        "📄 Application Fee ($)", min_value=0.0, step=25.0,
        key="calc_application", on_change=_save_form,
        help="Non-refundable fee for applying."
    )
with col4:
    administrative = st.number_input(
        "📋 Administrative Fee ($)", min_value=0.0, step=25.0,
        key="calc_admin", on_change=_save_form,
        help="Non-refundable fee for lease preparation."
    )

col5, col6 = st.columns(2)
with col5:
    house_type = st.selectbox(
        "🏠 Apartment Type", options=list(UTILITIES_AVG.keys()),
        key="calc_house_type", on_change=_save_form,
        help="Select your unit type to estimate utilities."
    )
with col6:
    roommates = st.number_input(
        "👥 Number of Roommates", min_value=0, max_value=10, step=1,
        key="calc_roommates", on_change=_save_form,
        help="Shared costs will be divided evenly among all residents."
    )

st.divider()

st.header("🚗 Transportation - First 60 Days")

transport_options = [
    "School shuttle (free)", "Public transport (bus/train)",
    "Uber / Lyft", "Walking", "Bike",
]
transport_mode = st.radio(
    "How will you mainly get around?",
    options=transport_options,
    key="calc_transport_mode", on_change=_save_form,
    help="Choose your primary mode of transportation."
)

transport_cost = 0
rides_per_day = 0

if transport_mode == "Public transport (bus/train)":
    rides_per_day = st.number_input(
        f"🚌 Average bus/streetcar rides per day ($1.25/ride):",
        min_value=0, max_value=20, step=1,
        key="calc_bus_rides",
        help=f"60-day cost: \${BUS_FARE_PER_RIDE} x rides/day x 60 days"
    )
    transport_cost = calculate_transport_cost(transport_mode, rides_per_day)
    st.info(f"📊 Estimated 60-day cost: **\\${transport_cost:.2f}**")

elif transport_mode == "Uber / Lyft":
    st.info("To estimate accurate ride costs, please visit the **Fare Estimator** page.")
    col_fare1, col_fare2 = st.columns([2, 1])
    with col_fare1:
        if st.session_state.get("uber_estimated_price"):
            st.success(f"Fare Estimator price loaded: **${st.session_state.uber_estimated_price:.2f}**/ride")
    with col_fare2:
        if st.button("Go to Fare Estimator", use_container_width=True):
            st.switch_page("pages/5_Fare_Estimator.py")

    # pre-fill uber cost from the Fare Estimator if the user hasn't changed it yet
    if st.session_state.get("uber_estimated_price") and st.session_state.calc_uber_cost == float(UBER_AVG_COST):
        st.session_state.calc_uber_cost = float(st.session_state.uber_estimated_price)

    col_uber1, col_uber2 = st.columns(2)
    with col_uber1:
        uber_cost_per_ride = st.number_input(
            "💵 Average cost per ride ($):", min_value=0.0, step=1.0,
            key="calc_uber_cost", on_change=_save_form,
            help="Typical rides in New Orleans range from $10-$20"
        )
    with col_uber2:
        rides_per_day = st.number_input(
            "🚕 Average rides per day:", min_value=0, max_value=20, step=1,
            key="calc_uber_rides", on_change=_save_form,
            help="Be realistic about your daily transportation needs"
        )
    transport_cost = calculate_transport_cost(transport_mode, rides_per_day, uber_cost_per_ride)

st.divider()

st.header("💵 Your Savings")

savings = st.number_input(
    "💰 Cash Available on Arrival ($)", min_value=0.0, step=100.0,
    key="calc_savings", on_change=_save_form,
    help="Total money you'll have when you arrive in New Orleans"
)

st.divider()

if "validation_errors" in st.session_state and st.session_state.validation_errors:
    st.error("⚠️ Please fix the following issues before calculating:")
    for error in st.session_state.validation_errors:
        st.markdown(f"- {error}")
    st.divider()

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    calculate_clicked = st.button(
        "🧮 Calculate Affordability",
        key="calculate_affordability",
        use_container_width=True,
        type="primary",
    )

if calculate_clicked:
    is_valid, error_messages = validate_inputs(rent, deposit, application, administrative, savings)

    if not is_valid:
        st.session_state.validation_errors = error_messages
        st.session_state.submitted = False
        st.session_state.calculation_results = None
        st.session_state.calculation_success = False
        st.session_state.show_results = False
        st.rerun()
    else:
        if "validation_errors" in st.session_state:
            del st.session_state.validation_errors
        try:
            day0, day60, remaining, breakdown = calculate_affordability(
                rent=rent, deposit=deposit, application=application,
                admin=administrative, unit_type=house_type,
                roommates=roommates, transport=transport_cost, savings=savings,
            )

            st.session_state.calculation_results = {
                "day0": day0, "day60": day60, "remaining": remaining,
                "breakdown": breakdown,
                "inputs": {
                    "rent": rent, "deposit": deposit, "application": application,
                    "admin": administrative, "unit_type": house_type,
                    "roommates": roommates, "transport": transport_cost,
                    "transport_mode": transport_mode, "savings": savings,
                }
            }

            st.session_state.submitted = True
            st.session_state.calculation_success = True
            st.session_state.show_results = True
            st.rerun()

        except Exception as e:
            st.error(f"❌ Calculation error: {str(e)}")
            st.session_state.submitted = False
            st.session_state.calculation_results = None

# results — only shown after the user clicks Calculate
if st.session_state.get("show_results", False) and st.session_state.get("calculation_results"):
    results = st.session_state.calculation_results
    day0 = results["day0"]
    day60 = results["day60"]
    remaining = results["remaining"]
    breakdown = results["breakdown"]
    inp = results["inputs"]

    st.divider()
    st.header("📊 Your Results")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💼 Cash needed at move-in", f"${day0:,.2f}",
                  help="Money needed on Day 0 to get keys")
    with col2:
        st.metric("📅 Total 60-day expenses", f"${day60:,.2f}",
                  help="All costs for first 2 months")
    with col3:
        delta_text = f"{(remaining / inp['savings'] * 100):.1f}% remaining" if inp["savings"] > 0 else None
        st.metric("💰 Balance after 60 days", f"${remaining:,.2f}",
                  delta=delta_text, help="Money left after first 60 days")

    st.divider()

    risk_level, risk_icon = get_risk_level(remaining, day60)

    if risk_level == "high":
        st.error(
            f"{risk_icon} **High Risk**: Your savings (\\${inp['savings']:,.2f}) don't cover the first 60 days "
            f"(\\${day60:,.2f}). You're short by **\\${abs(remaining):,.2f}**.",
            icon="🚨"
        )
    elif risk_level == "medium":
        st.warning(
            f"{risk_icon} **Low Buffer**: You'll have only \\${remaining:,.2f} left after 60 days. "
            f"Unexpected costs could cause financial stress.", icon="⚠️"
        )
    elif risk_level == "low":
        st.info(
            f"{risk_icon} **Moderate Buffer**: You'll have \\${remaining:,.2f} remaining. "
            f"Budgeting carefully is important.", icon="ℹ️"
        )
    else:
        st.success(
            f"{risk_icon} **Strong Buffer**: You'll have \\${remaining:,.2f} left after 60 days. "
            f"Well-positioned for the first 2 months!", icon="✅"
        )

    st.info(
        "📝 **Note**: This is an estimate based on average costs. Actual expenses may vary. "
        "Always budget for unexpected costs.", icon="💡"
    )

    st.divider()

    st.header("📊 Expense Breakdown (First 60 Days)")

    fig = px.pie(
        names=list(breakdown.keys()), values=list(breakdown.values()),
        title="Where Your Money Goes", hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(
        textinfo='none',
        hovertemplate='<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>'
    )
    fig.update_layout(showlegend=True, height=500, font=dict(size=13))
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 View Detailed Breakdown"):
        breakdown_df = pd.DataFrame([
            {"Category": k, "Amount": f"${v:,.2f}", "Percentage": f"{(v/day60*100):.1f}%"}
            for k, v in breakdown.items()
        ])
        st.dataframe(breakdown_df, hide_index=True, use_container_width=True)
        st.markdown(f"**Total 60-Day Cost:** ${day60:,.2f}")

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Save to My Results", use_container_width=True, type="primary"):
            st.switch_page("pages/2_My_Results.py")

    st.divider()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Start Over", use_container_width=True):
            for key in ["submitted", "calculation_results", "show_results", "calculation_success",
                        "calc_rent", "calc_deposit", "calc_application", "calc_admin",
                        "calc_house_type", "calc_roommates", "calc_transport_mode",
                        "calc_bus_rides", "calc_uber_rides", "calc_uber_cost",
                        "calc_savings", "_calc_form"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

if not st.session_state.get("show_results", False):
    st.caption(
        "💡 Made for students, by students | "
        "Data: [RentCafe](https://www.rentcafe.com/average-rent-market-trends/us/la/new-orleans/), "
        "[Expat Arrivals](https://www.expatarrivals.com/americas/usa/new-orleans/cost-living-new-orleans), "
        "[RTA/Token Transit](https://tokentransit.com/agency/neworleansrta), "
        "Entergy New Orleans | "
        "Questions? arrivalcalc@gmail.com"
    )
