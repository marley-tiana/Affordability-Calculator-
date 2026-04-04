import streamlit as st

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Student Advice",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# HEADER
# =============================================================================

st.title("Student Advice")
st.markdown("*Things students wish they knew before moving to New Orleans*")

st.divider()

# =============================================================================
# HELPER: render advice list + any session submissions
# =============================================================================

def render_advice(advice_list):
    for entry in advice_list:
        with st.expander(f"**{entry['tag']}**"):
            st.markdown(f'> *"{entry["quote"]}"*')
            st.markdown(f"<sub>— {entry['attribution']}</sub>", unsafe_allow_html=True)

# =============================================================================
# HOUSING TIPS
# =============================================================================

st.header("🏠 Housing Tips")

housing_advice = [
    {
        "tag": "Watch Out for Scams",
        "quote": (
            "Watch out for scams — especially on Facebook. There are a lot of AI-driven scam listings "
            "that look both cheap and really nice. Be extra cautious if a landlord won't allow an in-person "
            "visit. Some rents are unreasonably high too — if you're moving from New York, $2,000/month might "
            "seem fine, but it's a lot for New Orleans. The housing situation here takes some energy to navigate, "
            "so start early."
        ),
        "attribution": "PhD, 3rd year · China"
    },
    {
        "tag": "Choose a Walkable Location",
        "quote": "Try to live somewhere you're willing to walk to and from your most-visited spots.",
        "attribution": "Undergraduate, 3rd year · Honduras"
    },
    {
        "tag": "Where to Live First",
        "quote": (
            "Deming is a great first choice — it really helps with the transition. If you don't get in, "
            "try to find something near the uptown campus so you can use the shuttle. And always verify "
            "who you're renting from before booking anything."
        ),
        "attribution": "2nd year · India"
    },
    {
        "tag": "Renter's Insurance",
        "quote": "Research about renter's insurance.",
        "attribution": "PhD, 2nd year · China"
    },
    {
        "tag": "Negotiate a Shorter Lease",
        "quote": (
            "Try to get a shorter lease term if you can. That way, if you're not happy with your place "
            "after a semester, you have the flexibility to move. Buckle up!"
        ),
        "attribution": "MS · Nepal"
    },
    {
        "tag": "Apartment Selection Tips",
        "quote": "Do your best to avoid upstairs neighbors if you can.",
        "attribution": "MA, 2nd year · Ethiopia"
    },
]

render_advice(housing_advice)

st.divider()

# =============================================================================
# MOVING-IN TIPS
# =============================================================================

st.header("📦 Moving-In Tips")

moving_advice = [
    {
        "tag": "Plan Your Airport Arrival",
        "quote": (
            "Figure out how you'll get from the airport to your new place before you land. I bought a SIM "
            "card at the airport but the internet wasn't working, so once I left I had no connectivity. "
            "The Uber dropped me at the wrong location and I ended up walking in circles at 1 AM, which "
            "wasn't safe."
        ),
        "attribution": "PhD, 3rd year · Rwanda"
    },
    {
        "tag": "Pre-Arrival Checklist",
        "quote": (
            "Have a plan before you arrive. Housing usually requires a deposit, so have that ready. "
            "Make a list of what you'll need for your bedroom, bathroom, and kitchen — it helps you avoid "
            "forgetting things and buying stuff you don't need. Dollar Tree, Dollar General, and Walmart "
            "are your friends. Moving is stressful and costs add up fast. And always take advantage of "
            "university resources — sometimes you won't even know they exist until someone tells you, "
            "so connect with people and share your challenges."
        ),
        "attribution": "PhD · Ethiopia"
    },
    {
        "tag": "Furnish",
        "quote": "Most places come unfurnished.",
        "attribution": "PhD, 3rd year · Azerbaijan"
    },
    {
        "tag": "Shop Secondhand",
        "quote": "Get as many things secondhand as you can.",
        "attribution": "Bachelors, 4th year · Maryland"
    },
]

render_advice(moving_advice)

st.divider()

# =============================================================================
# LIFE IN NEW ORLEANS
# =============================================================================

st.header("🎭 Life in New Orleans")

life_advice = [
    {
        "tag": "Know the Safety Landscape",
        "quote": (
            "Tulane needs to do a better job informing students about crime in the downtown area before "
            "they arrive. Living in Deming, in downtown, can be dangerous, and students deserve to know "
            "that upfront."
        ),
        "attribution": "PhD, 4th year · Iran"
    },
    {
        "tag": "Find Your Community",
        "quote": (
            "Find your community as quickly as possible. They can be an incredible help for navigating "
            "life at Tulane, in New Orleans, and in the US in general."
        ),
        "attribution": "PhD, 4th year · Nigeria"
    },
    {
        "tag": "Neighborhoods & Parking",
        "quote": (
            "Know which neighborhoods students actually live in. New Orleans changes block by block, so "
            "having that mental map early makes life a lot easier. If you have a car, learn the parking "
            "rules immediately — the tickets here are no joke. Downtown parking is either impossible or "
            "expensive, so Uber is often the cheaper, less stressful option."
        ),
        "attribution": "Master's · Lima, Peru"
    },
    {
        "tag": "Getting Settled",
        "quote": (
            "Know which supermarket works best for your needs, and seriously consider living close to "
            "the uptown campus — the convenience is real. Share these kinds of tips with your country "
            "or continent's student organization too."
        ),
        "attribution": "PhD in Economics, 1st year · Bolivia"
    },
]

render_advice(life_advice)

st.divider()

# =============================================================================
# MONEY & BUDGETING
# =============================================================================

st.header("💰 Money & Budgeting")

money_advice = [
    {
        "tag": "Research Fees Early",
        "quote": (
            "I was very lucky overall, but I know other friends faced serious challenges. Do your research early about your costs so that you're not caught off guard."
        ),
        "attribution": "MA · Costa Rica"
    },
    {
        "tag": "Budget for Utilities & Outages",
        "quote": "Budget! Additionally, electricity will go out so have some battery-powered lights on hand.",
        "attribution": "4th year BArch · China"
    },
    {
        "tag": "Know Your University Fees",
        "quote": (
            "Get the exact breakdown of university fees at least two months before you arrive. "
            "Taxi and transport costs here are also higher than you might expect."
        ),
        "attribution": "MA, 1st year · Peru"
    },
]

render_advice(money_advice)

st.divider()

# =============================================================================
# SURVEY LINK
# =============================================================================

st.header("🗣️ Share Your Advice")

st.info(
    "Are you a current or former Tulane student? Share your advice for "
    "incoming students about housing, moving, and life in New Orleans. "
    "Responses are anonymous and help future students prepare better."
)

with st.container(border=True):
    st.subheader("Take the Survey")
    st.markdown("Takes about 5 minutes — completely anonymous:")
    st.link_button(
        "Take the Survey",
        "https://qualtricsxmwhclqpvzy.qualtrics.com/jfe/form/SV_0e0EOkK74FAXjXU",
        use_container_width=True
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "**What we're asking:**\n"
            "- Housing tips and warnings\n"
            "- Moving-in lessons learned\n"
            "- Money-saving strategies\n"
            "- Things you wish you knew"
        )
    with col2:
        st.markdown(
            "**How it works:**\n"
            "- Completely anonymous\n"
            "- Takes about 5 minutes\n"
            "- Helps future students\n"
            "- Updated regularly"
        )

st.divider()

st.caption(
    "💬 Student Advice | All advice is anonymous and based on student experiences | "
    "Made for students, by students"
)
