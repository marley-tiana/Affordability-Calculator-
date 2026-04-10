import streamlit as st

st.set_page_config(
    page_title="NOLA Housing Calculator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# show the landing question once per session before anything else
if "housing_status" not in st.session_state:
    st.title("Welcome to the NOLA Housing Calculator")
    st.markdown(
        "Before we get started, let us point you in the right direction."
    )
    st.divider()

    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        st.subheader("Have you found housing yet?")
        st.markdown(" ")

        if st.button(
            "Yes, I've found housing",
            type="primary",
            use_container_width=True,
            key="landing_yes",
        ):
            st.session_state.housing_status = "found"
            st.rerun()

        st.markdown(" ")

        if st.button(
            "No, I'm still searching",
            use_container_width=True,
            key="landing_no",
        ):
            st.session_state.housing_status = "searching"
            st.rerun()

    st.stop()

elif st.session_state.housing_status == "searching":
    st.switch_page("pages/9_Housing_Guide.py")
    st.stop()

# if housing_status == "found", fall through to the home page below

# build the savings numbers shown in the hero section
# sources: RentCafe (Jan 2026), Zumper (Feb 2026), RTA New Orleans

# 1-bed monthly rent by neighborhood
NEIGHBORHOOD_RENTS = {
    "Uptown": 1150,             # Zumper Feb 2026
    "Garden District": 1287,    # Zumper Feb 2026
    "Mid-City": 1491,           # RentCafe Jan 2026
    "French Quarter/CBD": 1838, # RentCafe Jan 2026
}

# transportation costs over 60 days
UBER_DAILY_COST = 15  # avg per ride
UBER_RIDES_PER_DAY = 1
UBER_60DAY = UBER_DAILY_COST * UBER_RIDES_PER_DAY * 60  # $900
JAZZY_PASS_MONTHLY = 45  # RTA unlimited 31-day pass
BUS_PASS_60DAY = JAZZY_PASS_MONTHLY * 2  # $90

# roommate savings (60-day, using 2-bed avg)
RENT_ALONE_1BED = 1264   # RentCafe citywide 1-bed avg (Jan 2026)
RENT_2BED_SPLIT = 1510 / 2  # RentCafe citywide 2-bed avg split with 1 roommate

highest_rent = max(NEIGHBORHOOD_RENTS.values())  # $1,838 (French Quarter)
lowest_rent = min(NEIGHBORHOOD_RENTS.values())   # $1,150 (Uptown)

# picking Uptown over French Quarter for 2 months
neighborhood_savings_60day = (highest_rent - lowest_rent) * 2  # $1,376

# splitting a 2-bed vs living alone in a 1-bed, over 2 months
roommate_savings_60day = (RENT_ALONE_1BED - RENT_2BED_SPLIT) * 2  # $1,018

# Jazzy Pass vs Uber 2x/week, over 2 months
uber_2x_weekly_monthly = 15 * 2 * 4.3  # ~$129/mo
transport_savings_60day = (uber_2x_weekly_monthly - JAZZY_PASS_MONTHLY) * 2  # ~$168

# grocery + furniture savings from the survival guide
grocery_savings_60day = (150 - 80) * 2 * 2  # expensive vs budget stores, 2 months = $280
furniture_savings = 300  # secondhand vs new

total_potential_savings = neighborhood_savings_60day + transport_savings_60day + grocery_savings_60day + furniture_savings


st.title("New Orleans Housing Calculator")
st.subheader("Plan Your First 60 Days with Confidence")
st.markdown(
    "A comprehensive financial planning tool for students moving to New Orleans. "
    "Estimate housing costs, save money with expert tips, and make informed decisions. "
    "**Built by students, for students.**"
)

st.divider()

st.header("What This Tool Offers")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Smart Calculator")
    st.markdown(
        "Calculate your first 60 days of housing expenses including rent, utilities, "
        "deposits, and transportation. Get instant affordability analysis."
    )

with col2:
    st.subheader("Money-Saving Tips")
    st.markdown(
        f"Learn how to save up to **${total_potential_savings:,.0f}** in your first 60 days "
        "with our comprehensive survival guide covering groceries, transportation, and furniture."
    )

with col3:
    st.subheader("Smart Analysis")
    st.markdown(
        "Compare neighborhoods, analyze roommate scenarios, estimate Uber fares, "
        "and save multiple calculations for easy comparison."
    )

st.divider()

st.header("Available Tools")

tool1, tool2 = st.columns(2)

with tool1:
    with st.container(border=True):
        st.subheader("Affordability Calculator")
        st.markdown(
            "Enter your housing details and get instant feedback on whether you can "
            "afford your first 60 days in New Orleans."
        )
        st.markdown(
            "- Move-in cost estimation\n"
            "- 60-day expense breakdown\n"
            "- Risk assessment\n"
            "- Visual expense charts"
        )
        if st.button("Open Calculator", key="tool_calc", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Calculator.py")

with tool2:
    with st.container(border=True):
        st.subheader("60-Day Survival Guide")
        st.markdown(
            "Expert tips and strategies to maximize savings during your first "
            "two months in New Orleans."
        )
        st.markdown(
            "- Grocery shopping strategies\n"
            "- Transportation hacks\n"
            "- Furniture tips\n"
            "- Student discounts"
        )
        if st.button("Open Survival Guide", key="tool_guide", use_container_width=True):
            st.switch_page("pages/3_Survival_Guide.py")

tool3, tool4 = st.columns(2)

with tool3:
    with st.container(border=True):
        st.subheader("Cost Analysis")
        st.markdown(
            "Compare different living scenarios to find the best option for your budget."
        )
        st.markdown(
            "- Neighborhood rent comparisons\n"
            "- Roommate cost scenarios\n"
            "- Annual savings breakdown\n"
            "- Living alone vs. with roommates"
        )
        if st.button("Open Cost Analysis", key="tool_cost", use_container_width=True):
            st.switch_page("pages/4_Cost_Analysis.py")

with tool4:
    with st.container(border=True):
        st.subheader("Fare Estimator")
        st.markdown(
            "Get instant Uber/Lyft fare estimates for trips around New Orleans "
            "using free geocoding."
        )
        st.markdown(
            "- Real driving distance & time\n"
            "- Fare breakdown (base, distance, time)\n"
            "- Alternative transport options\n"
            "- Google Maps route link"
        )
        if st.button("Open Fare Estimator", key="tool_fare", use_container_width=True):
            st.switch_page("pages/5_Fare_Estimator.py")

tool5, = st.columns(1)

with tool5:
    with st.container(border=True):
        st.subheader("Housing Training")
        st.markdown(
            "Step-by-step training modules to prepare you for every stage of the move — "
            "even if you've already found a place."
        )
        st.markdown(
            "- How to find and vet a rental\n"
            "- Property viewing checklist\n"
            "- Navigating deposits\n"
            "- Getting from the airport + Uber/Lyft setup + SIM cards"
        )
        if st.button("Open Housing Training", key="tool_housing", use_container_width=True):
            st.switch_page("pages/9_Housing_Guide.py")

st.divider()

st.header("By The Numbers")

stat1, stat2, stat3, stat4 = st.columns(4)

with stat1:
    st.metric("Potential 60-Day Savings", f"${total_potential_savings:,.0f}")
with stat2:
    st.metric("Planning Period", "60 Days")
with stat3:
    st.metric("Powerful Tools", "5")
with stat4:
    st.metric("Cost", "100% Free")

st.divider()

st.header("Why Use This Tool?")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown(
        "**Comprehensive & Accurate**\n"
        "- Based on real 2026 New Orleans data\n"
        "- Student survey insights\n"
        "- Regular updates\n\n"
        "**Completely Free**\n"
        "- No sign-up required\n"
        "- No credit card needed"
    )

with feature_col2:
    st.markdown(
        "**Student-Focused**\n"
        "- Built by students, for students\n"
        "- Tulane-specific insights\n"
        "- New Orleans local tips\n\n"
        "**Privacy-First**\n"
        "- No data collection\n"
        "- Browser-only storage\n"
        "- Secure & private"
    )

st.divider()

st.header("Ready to Plan Your Move?")
st.markdown("Start with the calculator to see your 60-day housing costs.")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Start Calculator Now", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Calculator.py")

st.divider()

st.caption(
    "🏠 **New Orleans Housing Calculator** | "
    "Made for students, by students | "
    "Contact us: arrivalcalc@gmail.com | "
    "Data: [RentCafe](https://www.rentcafe.com/average-rent-market-trends/us/la/new-orleans/), "
    "[Zumper](https://www.zumper.com/rent-research/new-orleans-la), "
    "[RTA/Token Transit](https://tokentransit.com/agency/neworleansrta), "
    "Entergy New Orleans | "
    "© 2026 | Free for student use"
)
