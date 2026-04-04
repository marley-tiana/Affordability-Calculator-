import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Cost Comparison",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# HEADER
# =============================================================================

st.title("Cost Comparison Tool")
st.markdown("*Compare different living scenarios and make informed decisions*")

st.info("Explore how different choices affect your budget")

st.divider()

# =============================================================================
# TAB LAYOUT
# =============================================================================

tab1, tab2 = st.tabs([
    "Neighborhoods",
    "Roommate Scenarios",
])

# ===== NEIGHBORHOODS TAB =====
with tab1:
    st.header("Neighborhood Cost Comparison")

    # Neighborhood rent data — sourced from Zumper (Feb 2026) and RentCafe (Jan 2026)
    # Citywide averages: 1-bed $1,264, 2-bed $1,510 (RentCafe Jan 2026)
    neighborhoods = {
        "Uptown (Near Campus)": {
            "rent_studio": 950,     # Zumper Feb 2026 (estimated from 1-bed ratio)
            "rent_1bed": 1150,      # Zumper Feb 2026
            "rent_2bed": 1675,      # Zumper Feb 2026
            "commute_time": "5-10 min walk",
            "walkability": "Excellent",
            "grocery_access": "Whole Foods, Rouses",
            "pros": ["Walking distance to campus", "Many student housing options", "Walkable neighborhood"],
            "cons": ["Higher rent for 2-bed", "Limited parking", "Can be quiet"],
            "source": "Zumper Feb 2026"
        },
        "Garden District": {
            "rent_studio": 1000,    # Zumper Feb 2026 (estimated from 1-bed ratio)
            "rent_1bed": 1287,      # Zumper Feb 2026
            "rent_2bed": 1650,      # Zumper Feb 2026
            "commute_time": "15-20 min shuttle",
            "walkability": "Good",
            "grocery_access": "Rouses, Whole Foods",
            "pros": ["Beautiful historic area", "Quieter than Uptown", "Good restaurants"],
            "cons": ["Need shuttle/bike for campus", "Tourist area"],
            "source": "Zumper Feb 2026"
        },
        "Mid-City": {
            "rent_studio": 1100,    # RentCafe Jan 2026 (estimated from avg)
            "rent_1bed": 1491,      # RentCafe Jan 2026
            "rent_2bed": 2078,      # RentCafe Jan 2026
            "commute_time": "25-30 min bus/car",
            "walkability": "Moderate",
            "grocery_access": "Walmart, Rouses, Costco",
            "pros": ["More space", "Diverse neighborhood", "Near City Park"],
            "cons": ["Longer commute", "Need reliable transport", "Variable by block"],
            "source": "RentCafe Jan 2026"
        },
        "French Quarter/CBD": {
            "rent_studio": 1400,    # RentCafe Jan 2026 (estimated from avg)
            "rent_1bed": 1838,      # RentCafe Jan 2026
            "rent_2bed": 3359,      # RentCafe Jan 2026
            "commute_time": "30-40 min streetcar",
            "walkability": "Excellent",
            "grocery_access": "Small markets, Rouses CBD",
            "pros": ["Heart of the city", "Very walkable", "Streetcar access"],
            "cons": ["Most expensive", "Very loud", "Long commute to campus", "Tourist crowds"],
            "source": "RentCafe Jan 2026"
        }
    }

    # Professional comparison DataFrame
    comparison_data = []
    for name, data in neighborhoods.items():
        comparison_data.append({
            "Neighborhood": name,
            "Studio": f"${data['rent_studio']:,}",
            "1-Bed": f"${data['rent_1bed']:,}",
            "2-Bed": f"${data['rent_2bed']:,}",
            "Commute to Campus": data['commute_time'],
            "Walkability": data['walkability'],
            "Grocery Access": data['grocery_access']
        })

    df_neighborhoods = pd.DataFrame(comparison_data)
    st.dataframe(df_neighborhoods, hide_index=True, use_container_width=True)

    st.markdown("---")

    # Key metrics row
    st.subheader("Quick Comparison")

    metric_cols = st.columns(4)
    for idx, (name, data) in enumerate(neighborhoods.items()):
        with metric_cols[idx]:
            short_name = name.split(" (")[0] if " (" in name else name.split("/")[0]
            st.metric(
                label=short_name,
                value=f"${data['rent_1bed']:,}/mo",
                delta=f"${data['rent_1bed'] - min(d['rent_1bed'] for d in neighborhoods.values()):+,} vs cheapest",
                delta_color="inverse"
            )

    st.markdown("---")

    # Rent comparison bar chart
    st.subheader("Rent Comparison by Apartment Type")

    fig = go.Figure()

    for apt_type, label in [('rent_studio', 'Studio'), ('rent_1bed', '1-Bed'), ('rent_2bed', '2-Bed')]:
        fig.add_trace(go.Bar(
            name=label,
            x=list(neighborhoods.keys()),
            y=[data[apt_type] for data in neighborhoods.values()],
            text=[f"${data[apt_type]:,}" for data in neighborhoods.values()],
            textposition='auto',
        ))

    fig.update_layout(
        barmode='group',
        title="Monthly Rent by Neighborhood",
        xaxis_title="Neighborhood",
        yaxis_title="Monthly Rent ($)",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Detailed neighborhood breakdown
    st.subheader("Detailed Neighborhood Breakdown")

    cols = st.columns(2)

    for idx, (name, data) in enumerate(neighborhoods.items()):
        with cols[idx % 2]:
            with st.expander(f"**{name}**", expanded=False):
                # Rent metrics
                rent_cols = st.columns(3)
                with rent_cols[0]:
                    st.metric("Studio", f"${data['rent_studio']:,}")
                with rent_cols[1]:
                    st.metric("1-Bed", f"${data['rent_1bed']:,}")
                with rent_cols[2]:
                    st.metric("2-Bed", f"${data['rent_2bed']:,}")

                st.markdown(f"""
**Location Details:**
- Commute to Campus: {data['commute_time']}
- Walkability: {data['walkability']}
- Grocery Access: {data['grocery_access']}

**Pros:** {', '.join(data['pros'])}

**Cons:** {', '.join(data['cons'])}
                """)

# ===== ROOMMATE SCENARIOS TAB =====
with tab2:
    st.header("Living Alone vs. With Roommates")

    st.markdown("""
    One of the biggest factors in your monthly costs is whether you live alone or with roommates.
    Let's see how it affects your budget:
    """)

    # Interactive comparison
    col1, col2 = st.columns(2)

    with col1:
        example_rent = st.slider(
            "Your Monthly Rent ($)",
            min_value=800,
            max_value=3000,
            value=1264,
            step=50,
            help="Enter the monthly rent for a 1-bedroom apartment"
        )

    with col2:
        deposit_amount = st.slider(
            "Security Deposit ($)",
            min_value=500,
            max_value=3000,
            value=1264,
            step=50
        )

    # Utility estimates based on Expat Arrivals & Entergy New Orleans data
    # Basic utilities ~$207/mo + internet ~$65/mo = ~$272/mo for 1-bed
    # Rent ratios based on RentCafe Jan 2026 citywide averages:
    # 1-bed $1,264, 2-bed $1,510 (ratio ~1.19x), 3-bed ~1.45x, 4-bed ~1.60x

    # Calculate scenarios — user enters their 1-bed rent, we scale up for larger units
    scenarios = {
        "Living Alone (1-bed)": {
            "rent": example_rent,
            "utilities": 272,  # 1-bed avg (Expat Arrivals + internet)
            "deposit": deposit_amount,
            "roommates": 0
        },
        "1 Roommate (2-bed)": {
            "rent": (example_rent * 1.19) / 2,  # 2-bed is ~1.19x of 1-bed, split 2 ways
            "utilities": 313 / 2,
            "deposit": (deposit_amount * 1.19) / 2,
            "roommates": 1
        },
        "2 Roommates (3-bed)": {
            "rent": (example_rent * 1.45) / 3,  # 3-bed is ~1.45x of 1-bed, split 3 ways
            "utilities": 354 / 3,
            "deposit": (deposit_amount * 1.45) / 3,
            "roommates": 2
        },
        "3 Roommates (4-bed)": {
            "rent": (example_rent * 1.60) / 4,  # 4-bed is ~1.60x of 1-bed, split 4 ways
            "utilities": 395 / 4,
            "deposit": (deposit_amount * 1.60) / 4,
            "roommates": 3
        }
    }

    # Calculate totals
    for scenario, data in scenarios.items():
        monthly_total = data["rent"] + data["utilities"]
        data["monthly_total"] = monthly_total
        data["sixty_day_total"] = monthly_total * 2
        data["year_total"] = monthly_total * 12

    # Display comparison
    st.subheader("Cost Breakdown")

    comparison_cols = st.columns(len(scenarios))

    for idx, (scenario, data) in enumerate(scenarios.items()):
        with comparison_cols[idx]:
            st.markdown(f"#### {scenario}")
            st.metric("Monthly", f"${data['monthly_total']:.0f}")
            st.metric("Move-in Cost", f"${data['rent'] + data['deposit']:.0f}")
            st.metric("First 60 Days", f"${data['sixty_day_total']:.0f}")
            st.metric("First Year", f"${data['year_total']:.0f}")

    st.markdown("---")

    # Savings visualization
    st.subheader("Annual Savings by Living Situation")

    alone_cost = scenarios["Living Alone (1-bed)"]["year_total"]

    savings_data = []
    for scenario, data in scenarios.items():
        savings = alone_cost - data["year_total"]
        savings_data.append({
            "Scenario": scenario,
            "Annual Cost": data["year_total"],
            "Savings vs Living Alone": max(0, savings)
        })

    df_savings = pd.DataFrame(savings_data)

    fig2 = px.bar(
        df_savings,
        x="Scenario",
        y="Savings vs Living Alone",
        title="How Much You Save Per Year by Having Roommates",
        text="Savings vs Living Alone",
        color="Savings vs Living Alone",
        color_continuous_scale="Greens"
    )

    fig2.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig2.update_layout(height=400, showlegend=False)

    st.plotly_chart(fig2, use_container_width=True)

    st.success(f"""
    **Key Insight**: Living with 1 roommate saves you approximately
    **\\${scenarios['Living Alone (1-bed)']['year_total'] - scenarios['1 Roommate (2-bed)']['year_total']:.0f}/year**
    compared to living alone!
    """)

    # Pros and cons
    st.subheader("Pros & Cons")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Living Alone**
        - Complete privacy
        - Your own space and rules
        - No roommate conflicts
        - Quieter environment
        - Much more expensive
        - All bills on you
        - Loneliness risk
        - No cost sharing for furniture
        """)

    with col2:
        st.markdown("""
        **Living with Roommates**
        - Save $4,000-8,000/year
        - Split utilities & internet
        - Built-in social network
        - Share furniture costs
        - Less privacy
        - Potential conflicts
        - Shared bathroom/kitchen
        - Compromise on lifestyle
        """)

st.divider()

# Footer
st.markdown("---")
st.caption(
    "All costs are estimates based on 2026 New Orleans averages. "
    "Neighborhood rents: [RentCafe](https://www.rentcafe.com/average-rent-market-trends/us/la/new-orleans/) (Jan 2026), "
    "[Zumper](https://www.zumper.com/rent-research/new-orleans-la) (Feb 2026). "
    "Utilities: [Expat Arrivals](https://www.expatarrivals.com/americas/usa/new-orleans/cost-living-new-orleans), Entergy New Orleans. "
    "Transit: [RTA/Token Transit](https://tokentransit.com/agency/neworleansrta). "
    "Your actual costs may vary based on lifestyle and choices."
)
