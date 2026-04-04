import streamlit as st

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="About & Help",
    page_icon="ℹ️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# HEADER
# =============================================================================

st.title("About This Tool")
st.markdown("*Everything you need to know about the Arrival Shock Calculator*")

st.info("Learn how to use this calculator effectively and understand your results")

st.divider()

# =============================================================================
# TABS
# =============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(["How to Use", "FAQs", "About the Data", "Housing Resources", "Contact & Feedback"])

# ===== HOW TO USE TAB =====
with tab1:
    st.header("How to Use This Calculator")

    st.subheader("Step-by-Step Guide")

    with st.expander("**Step 1: Gather Your Information**", expanded=True):
        st.markdown("""
        Before you start, collect these documents and information:

        **From Your Lease Agreement:**
        - Monthly rent amount
        - Security deposit
        - Application fee
        - Administrative/processing fee
        - Apartment type (studio, 1-bed, 2-bed, 3-bed, 4-bed)

        **Personal Information:**
        - Number of roommates (if any)
        - Total savings you'll have upon arrival
        - Your planned mode of transportation

        **Tip**: If you don't have exact numbers yet, use estimates from apartment listings
        """)

    with st.expander("**Step 2: Enter Your Housing Costs**"):
        st.markdown("""
        Navigate to the **Calculator** page and fill in:

        1. **Monthly Rent**: Enter the TOTAL rent before dividing with roommates
           - Correct: Enter $1,800 if that's the total rent
           - Incorrect: Don't enter $900 (your split portion)

        2. **Security Deposit**: Usually equal to one month's rent
           - This is refundable at move-out (if no damages)

        3. **Application Fee**: One-time, non-refundable fee
           - Typically $50-150

        4. **Administrative Fee**: One-time fee for processing
           - Typically $100-300

        5. **Apartment Type**: Select studio, 1-bed, 2-bed, 3-bed, or 4-bed
           - This determines utility estimates

        6. **Number of Roommates**: Enter 0 if living alone
           - The calculator will split costs automatically
        """)

    with st.expander("**Step 3: Select Transportation**"):
        st.markdown("""
        Choose your primary mode of transportation:

        **Free Options:**
        - School shuttle (free)
        - Walking
        - Bike

        **Paid Options:**
        - Public transport (bus/streetcar) - Enter average rides per day
        - Uber/Lyft - Enter average cost per ride AND rides per day
        - Scooter - Enter average rides per day

        **Tip**: Be realistic! Most students overestimate how often they'll Uber
        """)

    with st.expander("**Step 4: Enter Your Savings**"):
        st.markdown("""
        Enter the TOTAL cash you'll have when you arrive in New Orleans.

        Include:
        - Bank account balance
        - Cash on hand
        - Money from parents/family
        - Student loan refunds (if applicable)

        Do NOT include:
        - Future income (jobs you'll get later)
        - Money that's not accessible yet
        - Credit card limits
        """)

    with st.expander("**Step 5: Calculate and Review Results**"):
        st.markdown("""
        Click "Calculate Affordability" to see:

        1. **Cash Needed at Move-In**: Money you need on Day 0
        2. **Total 60-Day Expenses**: All costs for first 2 months
        3. **Balance After 60 Days**: How much money you'll have left

        The calculator will also show you:
        - Risk level (High/Medium/Low/None)
        - Expense breakdown pie chart
        """)

    with st.expander("**Step 6: Explore Other Pages**"):
        st.markdown("""
        After calculating, check out:

        **Survival Guide**: Learn how to save money on groceries, transport, furniture

        **Cost Comparison**: Compare neighborhoods, roommate scenarios, transport options
        """)

    st.markdown("---")

    st.subheader("Visual Guide")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **What the Calculator Does:**
        - Estimates your move-in costs
        - Calculates 60-day expenses
        - Shows remaining budget
        - Assesses financial risk
        - Provides tips
        """)

    with col2:
        st.markdown("""
        **What It Doesn't Include:**
        - Food/groceries
        - Personal items (clothes, toiletries)
        - Entertainment
        - Books/supplies
        - Health insurance
        - Emergency expenses
        """)

# ===== FAQs TAB =====
with tab2:
    st.header("Frequently Asked Questions")

    faqs = [
        {
            "q": "Why does the calculator ask for TOTAL rent, not my share?",
            "a": "We need the total to accurately calculate your portion when divided by roommates. The calculator automatically splits shared costs (rent, utilities) but keeps personal costs (transportation) separate."
        },
        {
            "q": "Are utilities included in the calculation?",
            "a": "Yes! The calculator uses average utility + internet costs for New Orleans based on apartment type (source: Expat Arrivals, Entergy New Orleans). Studios average \\$230/month, 1-beds \\$272/month, 2-beds \\$313/month, 3-beds \\$354/month, and 4-beds \\$395/month. These include electricity, water, gas, and internet."
        },
        {
            "q": "What if I don't know my exact transportation costs yet?",
            "a": "Make your best estimate. You can always recalculate later. Consider: Will you mainly walk/shuttle (free), take occasional Ubers (\\$60-100/month), or rely heavily on Uber (\\$200+/month)?"
        },
        {
            "q": "Why is my 60-day cost so much higher than monthly rent?",
            "a": "Move-in costs include one-time fees (security deposit, application fee, admin fee, wifi setup) PLUS two months of rent and utilities. It's normal for the first 60 days to cost 2.5-3x your normal monthly rent."
        },
        {
            "q": "What does 'High Risk' mean?",
            "a": "High Risk means your savings don't cover your estimated 60-day expenses. You may need to:\n- Increase your savings before arrival\n- Find cheaper housing\n- Get a roommate to split costs\n- Secure a part-time job quickly"
        },
        {
            "q": "Should I include student loan money in my savings?",
            "a": "Only if the loan refund will be available BEFORE you need to pay rent. Many students don't receive loan refunds until 2-3 weeks into the semester. Plan accordingly!"
        },
        {
            "q": "The calculator shows I'll have $0 left after 60 days. Is that bad?",
            "a": "Yes, that's risky! You should aim to have at least 10-20% of your 60-day expenses remaining as a buffer for:\n- Unexpected costs\n- Medical emergencies\n- Lost/stolen items\n- Academic expenses"
        },
        {
            "q": "Can I save the results or print them?",
            "a": "Your results are stored in your browser session while you're on the site. Take a screenshot or write down the numbers if you need them later. The results remain available as you navigate between pages."
        },
        {
            "q": "How accurate is this calculator?",
            "a": "The calculator uses real 2026 New Orleans cost data and student surveys. However, individual circumstances vary. Your actual costs may be 10-20% higher or lower depending on your lifestyle, location, and choices."
        },
        {
            "q": "What if my apartment is furnished?",
            "a": "Great! You'll save the $300 furniture cost mentioned in the Survival Guide. However, the main calculator doesn't include furniture costs anyway - it focuses only on essential housing and transportation expenses for the first 60 days."
        }
    ]

    for faq in faqs:
        with st.expander(f"**{faq['q']}**"):
            st.markdown(faq['a'])

    st.markdown("---")

    st.info("""
    **Still have questions?**

    - Check the Survival Guide for money-saving tips
    - Compare different scenarios in the Cost Comparison tool
    - Contact Tulane Housing Services
    - Join Tulane student Facebook groups
    """)

# ===== ABOUT THE DATA TAB =====
with tab3:
    st.header("About Our Data")

    st.markdown("""
    This calculator is built on real data from New Orleans and Tulane students.
    Here's where our numbers come from:
    """)

    st.subheader("Housing Cost Data")

    st.markdown("""
    **Rent Estimates (Neighborhood-Specific):**
    - Uptown: 1-bed $1,150/mo (Source: [Zumper](https://www.zumper.com/rent-research/new-orleans-la/uptown), Feb 2026)
    - Garden District: 1-bed $1,287/mo (Source: [Zumper](https://www.zumper.com/rent-research/new-orleans-la/garden-district), Feb 2026)
    - Mid-City: 1-bed $1,491/mo (Source: [RentCafe](https://www.rentcafe.com/average-rent-market-trends/us/la/new-orleans/mid-city-new-orleans/), Jan 2026)
    - French Quarter/CBD: 1-bed $1,838/mo (Source: [RentCafe](https://www.rentcafe.com/average-rent-market-trends/us/la/new-orleans/french-quarter/), Jan 2026)
    - Citywide averages: 1-bed \$1,264/mo, 2-bed \$1,510/mo (Source: [RentCafe](https://www.rentcafe.com/average-rent-market-trends/us/la/new-orleans/), Jan 2026)

    **Utility + Internet Averages:**
    - Basic utilities (electricity, water, gas): ~$207/mo for 915 sq ft (Source: [Expat Arrivals](https://www.expatarrivals.com/americas/usa/new-orleans/cost-living-new-orleans))
    - Internet: ~$65/month (Source: [Expat Arrivals](https://www.expatarrivals.com/americas/usa/new-orleans/cost-living-new-orleans))
    - Combined estimates by apartment size:
    - Studio: \$230/month average
    - 1-Bedroom: \$272/month average
    - 2-Bedroom: \$313/month average
    - 3-Bedroom: \$354/month average *(estimate)*
    - 4-Bedroom: \$395/month average *(estimate)*

    **Other Costs:**
    - Wi-Fi setup fee: $100 (router/modem setup)
    - Security deposits: Typically = 1 month rent
    - Application fees: Range from $50-150
    - Administrative fees: Range from $100-300
    """)

    st.subheader("Transportation Data")

    st.markdown("""
    **Public Transportation** (Source: [RTA/Token Transit](https://tokentransit.com/agency/neworleansrta)):
    - Streetcar/Bus: \$1.25/ride with free transfers (official RTA rate)
    - 1-Day Jazzy Pass: \$3.00 | 3-Day: \$8.00 | 7-Day: \$15.00
    - 31-Day Jazzy Pass: \$45.00 (unlimited rides on buses, streetcars, ferries)
    - Youth 31-Day Pass: \$18.00 | Priority (65+/Disabled): \$14.00
    - Tulane Shuttle: Free for all students

    **Ride-Sharing:**
    - Uber/Lyft averages based on student survey data
    - Typical ride range: $10-20 depending on distance
    - Surge pricing can double costs during peak hours
    - Fare Estimator uses [OSRM](http://project-osrm.org/) for real driving distances

    """)

    st.subheader("Grocery & Living Costs")

    st.markdown("""
    **Grocery Store Data:**
    - Based on student shopping surveys (updated 2026)
    - Comparison of typical student shopping cart
    - Prices collected from actual stores in New Orleans

    **Note:** The main calculator does NOT include food costs - only housing and
    transportation. Grocery savings are shown in the Survival Guide.
    """)

    st.subheader("Data Updates")

    st.markdown("""
    We update this calculator:
    - **Quarterly**: Rent and utility estimates
    - **Annually**: Major data refresh
    - **As needed**: When significant market changes occur

    Last updated: **February 2026**
    """)

    st.warning("""
    **Important Disclaimer**

    This calculator provides ESTIMATES based on average costs. Your actual expenses
    may vary significantly based on:
    - Your specific apartment/neighborhood
    - Your lifestyle and choices
    - Seasonal variations (utilities higher in summer)
    - Unexpected expenses
    - Changes in market conditions

    Always budget for 10-20% above estimated costs as a safety buffer!
    """)

# ===== HOUSING RESOURCES TAB =====
with tab4:
    st.header("Apartment Listing Sites & Housing Resources")

    st.markdown(
        "Use these verified resources to search for apartments in New Orleans. "
        "We recommend checking multiple sites to compare prices and availability."
    )

    st.subheader("Tulane University Housing")

    with st.expander("**Deming Pavilion — Tulane Graduate & International Student Housing**", expanded=True):
        st.markdown(
            "The Bertie M. and John W. Deming Pavilion is Tulane's on-campus graduate housing "
            "complex located on the downtown campus in the medical district.\n\n"
            "**What's Included in Rent:**\n"
            "- Basic cable, internet, electricity, and water\n\n"
            "**Unit Types:** Studios (small & large), 1-bed/1-bath, 2-bed/1-bath, 2-bed/2-bath "
            "(300 apartments total)\n\n"
            "**How to Apply:** Online through the Tulane Housing Portal. "
            "There is usually a waiting list, so apply as soon as you decide to attend Tulane.\n\n"
            "**Connected to the free Tulane shuttle system.**\n\n"
            "Website: [deming.tulane.edu](https://deming.tulane.edu/) | "
            "Apply: [housing.tulane.edu/graduate-housing](https://housing.tulane.edu/graduate-housing)"
        )

    with st.expander("**Tulane Off-Campus Housing Portal**"):
        st.markdown(
            "Tulane's official off-campus housing search tool with map-based search, "
            "roommate finder, sublet listings, and renter resources.\n\n"
            "Website: [offcampushousing.tulane.edu](https://offcampushousing.tulane.edu/)"
        )

    with st.expander("**Tulane Housing & Residence Life**"):
        st.markdown(
            "Off-Campus Housing resources, guides, and agencies/services recommended by Tulane.\n\n"
            "- [Off-Campus Housing Guide](https://housing.tulane.edu/off-campus-housing)\n"
            "- [Agencies & Services](https://housing.tulane.edu/off-campus-housing/agencies-and-services)\n"
            "- [Resources for Renters](https://housing.tulane.edu/off-campus-housing/resources)"
        )

    st.divider()

    st.subheader("Apartment Listing Websites")

    st.markdown("These major platforms list apartments available in New Orleans:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "**General Listings:**\n"
            "- [Apartments.com](https://www.apartments.com/new-orleans-la/) — 4,000+ listings, virtual tours\n"
            "- [Zillow Rentals](https://www.zillow.com/new-orleans-la/rentals/) — Filter by neighborhood & price\n"
            "- [Trulia](https://www.trulia.com/for_rent/New_Orleans,LA/) — Neighborhood insights & school info\n"
            "- [RentCafe](https://www.rentcafe.com/apartments-for-rent/us/la/new-orleans/) — Verified listings, rent trends\n"
            "- [Rent.com](https://www.rent.com/louisiana/new-orleans-apartments/) — Reviews & price tracking"
        )

    with col2:
        st.markdown(
            "**Student-Focused:**\n"
            "- [ApartmentList](https://www.apartmentlist.com/la/new-orleans) — Personalized matching\n"
            "- [Apartment Finder](https://www.apartmentfinder.com/Louisiana/New-Orleans-Apartments) — Near-campus filter\n"
            "- [CollegeStudentApartments.com](https://www.collegestudentapartments.com/city/new-orleans-louisiana/apartments/) — Student-only listings\n\n"
            "**Local Property Management:**\n"
            "- [1st Lake Properties](https://1stlake.com/) — Specializes in Greater New Orleans area apartments"
        )

    st.divider()

    st.subheader("Other Ways to Find Housing")

    st.markdown(
        "- **Facebook Groups:** Search for \"Tulane Classifieds\" or \"Tulane Free & For Sale\" "
        "for sublets and roommate postings\n"
        "- **Craigslist New Orleans:** [neworleans.craigslist.org/apa](https://neworleans.craigslist.org/search/apa) "
        "— Use caution and never send money before seeing a unit in person\n"
        "- **Tulane OISS:** The Office of International Students and Scholars provides "
        "housing guidance for international students — [oiss.tulane.edu/off-campus-housing](https://oiss.tulane.edu/off-campus-housing)\n"
        "- **TULAP:** Tulane University Legal Assistance Program offers free legal advice "
        "on lease questions for current students"
    )

    st.warning(
        "Always visit an apartment IN PERSON before signing a lease. "
        "Never wire money or pay a deposit without seeing the unit. "
        "Verify the landlord's identity and check reviews online."
    )

# ===== CONTACT & FEEDBACK TAB =====
with tab5:
    st.header("Contact & Feedback")

    st.markdown("""
    This tool was created by students, for students. We're constantly working to
    improve it based on your feedback!
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Send Feedback

        We'd love to hear from you:

        **Found a bug?** Contact us: arrivalcalc@gmail.com

        **Have suggestions?**
        - What features would help you?
        - What information is missing?
        - How can we make it better?

        **Want to contribute data?**
        - Share your actual costs (anonymous)
        - Help future students with real numbers
        - Update grocery/transport prices
        """)

    with col2:
        st.markdown("""
        ### Get Help

        **For Housing Questions:**
        - Tulane Housing & Residence Life
        - Phone: (504) 865-5724
        - [housing.tulane.edu](https://housing.tulane.edu)

        **For Financial Questions:**
        - Office of Financial Aid
        - Phone: (504) 865-5723
        - [financialaid.tulane.edu](https://financialaid.tulane.edu)

        **For General Student Support:**
        - Student Affairs
        - Case Management & Victim Support Services
        """)

    st.divider()

    st.subheader("Share This Tool")

    st.markdown("""
    Know someone moving to New Orleans for college? Share this calculator with them!

    This tool is especially helpful for:
    - Incoming freshmen
    - Transfer students
    - International students
    - Graduate students
    - Parents helping with planning
    - Students considering off-campus housing
    """)

    st.divider()

    st.subheader("Acknowledgments")

    st.markdown("""
    **Built with data and insights from:**
    - Tulane University Office of International Students and Scholars
    - Tulane University students (survey respondents)
    - Tulane Housing & Residence Life
    - [RentCafe](https://www.rentcafe.com/average-rent-market-trends/us/la/new-orleans/) — Neighborhood Rent Data (Jan 2026)
    - [Zumper](https://www.zumper.com/rent-research/new-orleans-la) — Neighborhood Rent Data (Feb 2026)
    - [Expat Arrivals](https://www.expatarrivals.com/americas/usa/new-orleans/cost-living-new-orleans) — Utility & Cost of Living Data
    - [RTA / Token Transit](https://tokentransit.com/agency/neworleansrta) — Official Transit Fares & Jazzy Pass Pricing
    - Entergy New Orleans — Electricity & Utility Rates
    - [OSRM](http://project-osrm.org/) — Driving Distance & Route Data
    - Local grocery stores and businesses

    **Special thanks to:**
    - Students who shared their real cost data
    - Tulane staff who provided guidance
    - Everyone who tested and provided feedback

    **Technology:**
    - Built with Streamlit (Python web framework)
    - Data visualization with Plotly
    - Hosted for free student access
    """)

st.divider()

# =============================================================================
# VERSION INFO
# =============================================================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Version**: 2.0
    **Last Updated**: February 2026
    """)

with col2:
    st.markdown("""
    **Data Sources**: Verified
    **Calculation Method**: Tested
    """)

with col3:
    st.markdown("""
    **License**: Free for student use
    **Privacy**: No data collected
    """)

# Footer
st.markdown("---")
st.caption("Made for students, by students. Helping Tulane students make informed housing decisions since 2026.")
