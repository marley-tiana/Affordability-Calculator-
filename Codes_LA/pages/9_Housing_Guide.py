import streamlit as st
import os

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Housing Training",
    page_icon="🏘️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =============================================================================
# HEADER
# =============================================================================

st.title("Housing Training")
st.markdown(
    "This isn't just a reading guide — it's a training walkthrough. "
    "Each module walks you through real scenarios so you're prepared before "
    "you ever talk to a landlord or sign a lease."
)

st.divider()

# =============================================================================
# THREE TRAINING MODULES
# =============================================================================

mod1, mod2, mod3 = st.tabs([
    "🔍 Module 1: Finding Housing",
    "🏠 Module 2: Viewing a Property",
    "💵 Module 3: Deposits",
])


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1: FINDING HOUSING
# ─────────────────────────────────────────────────────────────────────────────

with mod1:
    st.subheader("Where do you actually find housing?")
    st.markdown(
        "Most students waste time on the wrong platforms. Here's what works "
        "in New Orleans specifically:"
    )

    with st.expander("The Platforms That Actually Work", expanded=True):
        st.markdown(
            "| Platform | Best For | Watch Out For |\n"
            "|---|---|---|\n"
            "| **Tulane Off-Campus Housing Board** | Student-to-student listings near campus | Fills up fast — check daily |\n"
            "| **Zillow / Zumper / Apartments.com** | Browsing a wide inventory by price & neighborhood | Listed prices don't include utilities |\n"
            "| **Facebook Groups** ('Tulane Housing', 'New Orleans Student Rentals') | Sublets, roommate searches, quick finds | Verify the person is real before paying anything |\n"
            "| **Craigslist New Orleans** | Cheaper listings, older buildings | Higher scam risk — always tour in person |\n"
            "| **Word of mouth / GroupMe** | Getting a unit before it's publicly listed | You need to be in the right groups early |\n"
        )

    with st.expander("Neighborhoods & Price Ranges"):
        st.markdown(
            "| Neighborhood | Avg 1-Bed/mo | Reality Check |\n"
            "|---|---|---|\n"
            "| **Uptown** | ~$1,150 | Closest to campus — most popular for students |\n"
            "| **Garden District** | ~$1,287 | Beautiful streets, walkable, slightly quieter |\n"
            "| **Mid-City** | ~$1,491 | More affordable vibe, but you'll need a bus or car |\n"
            "| **French Quarter / CBD** | ~$1,838 | Lively but expensive and far from main campus |\n"
        )

    st.divider()
    st.subheader("Scenario Check — Module 1")

    st.info(
        "**Scenario:** You're moving to New Orleans in 3 months. "
        "Your max budget is \\$1,200/month. You want to be close to campus "
        "and don't have a car. A listing on Craigslist in Uptown is \\$950/month — "
        "well below market. The landlord says they're traveling and will mail you the keys "
        "after you Venmo the first month's rent and deposit."
    )

    q1 = st.radio(
        "What do you do?",
        options=[
            "Send the money — it's a great deal and Uptown is the right area",
            "Ask for a virtual tour first, then decide",
            "Do not send money — this is a textbook rental scam",
            "Ask a friend to check it out on your behalf before paying",
        ],
        index=None,
        key="mod1_q1",
    )

    if q1 == "Do not send money — this is a textbook rental scam":
        st.success(
            "Correct. Never send money — Venmo, Zelle, or cash — to a landlord "
            "you haven't met in person or verified. 'Traveling and will mail keys' "
            "is one of the most common rental scam scripts. A price well below market "
            "in a desirable area is the first red flag. Walk away."
        )
    elif q1 == "Ask for a virtual tour first, then decide":
        st.warning(
            "Getting closer — a virtual tour is better than nothing, but scammers "
            "can fake these too using photos stolen from real listings. The real issue "
            "here is the payment method (Venmo) and the landlord's unavailability. "
            "Never send money before you can verify the person owns or manages the property."
        )
    elif q1 is not None:
        st.error(
            "This is a scam. The combination of below-market price, urgent payment "
            "request, and an unavailable landlord who wants Venmo are all classic signals. "
            "Legitimate landlords do not ask for deposits before you've toured the unit "
            "and signed a lease."
        )

    st.divider()
    st.info(
        "**Quick Check:** Which of these is the most important thing to do "
        "before you start seriously browsing listings?"
    )

    q2 = st.radio(
        "Before browsing:",
        options=[
            "Save every listing you see so you don't forget them",
            "Know your actual budget — including utilities, not just rent",
            "Pick your favorite neighborhood and only look there",
            "Get on Zillow and apply to the first place you like",
        ],
        index=None,
        key="mod1_q2",
    )

    if q2 == "Know your actual budget — including utilities, not just rent":
        st.success(
            "Exactly. A $1,200/month apartment with $200 in utilities is a $1,400/month "
            "commitment. Many students forget this and end up rent-stressed by month two. "
            "Use the calculator on this site to map out your full 60-day costs first."
        )
    elif q2 is not None:
        st.error(
            "The most common mistake students make is treating the listed rent as the "
            "full cost. Before you browse, know your total budget including utilities "
            "(electricity in New Orleans summers can be $150–$200/month alone)."
        )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 2: VIEWING A PROPERTY
# ─────────────────────────────────────────────────────────────────────────────

with mod2:
    st.subheader("What do you actually look for when you visit?")
    st.markdown(
        "Most first-time renters focus on how the place looks. "
        "What you actually need to check is what the landlord hopes you won't notice."
    )

    with st.expander("What to Check During a Tour (and Why)", expanded=True):
        st.markdown(
            "**Safety — check these first**  \n"
            "- Do all door and window locks work? Test them yourself.  \n"
            "- Are smoke detectors present? (Required by law in Louisiana)  \n"
            "- Is the building well-lit at night? Drive by after dark if you can.  \n\n"
            "**Condition — New Orleans-specific issues**  \n"
            "- Look for water stains on ceilings or walls — mold follows water damage  \n"
            "- Run the faucets and flush the toilet — check water pressure  \n"
            "- Turn on the AC. If it's 'a little noisy' in June, it's broken in July.  \n"
            "- Look in corners and under the sink for signs of roaches or mice  \n\n"
            "**Practical — what you'll feel after week one**  \n"
            "- Is there in-unit laundry, or will you haul bags to a laundromat?  \n"
            "- Is there a bus stop within walking distance?  \n"
            "- What's the cell signal like inside the apartment?  \n"
            "- What internet providers service the building?"
        )

    with st.expander("Questions to Ask the Landlord"):
        st.markdown(
            "Ask these out loud during the tour — their answers (and hesitations) tell you a lot:  \n\n"
            "- What utilities are included in rent?  \n"
            "- How do I submit a maintenance request, and what's the average response time?  \n"
            "- Has this unit had any flooding or water damage?  \n"
            "- Has there been any pest treatment in the last year?  \n"
            "- Can I see a copy of the lease before I decide?"
        )

    st.divider()
    st.subheader("Scenario Check — Module 2")

    st.info(
        "**Scenario:** You're touring a 1-bedroom in Uptown. The rent is \\$1,100/month "
        "— right in your budget. The apartment smells a little musty, there's a brownish "
        "stain on the bedroom ceiling the landlord says is 'old and fixed,' and the AC "
        "rattles loudly but 'works fine.' The landlord says you need to decide today "
        "because two other people are looking at it this afternoon."
    )

    q3 = st.radio(
        "What's your move?",
        options=[
            "Sign it — the price is right and Uptown is where you want to be",
            "Ask for 24 hours to decide, and come back to check the AC and ceiling yourself",
            "Walk away — the combination of signs here is too risky",
            "Negotiate the rent down to account for the AC issue, then sign",
        ],
        index=None,
        key="mod2_q1",
    )

    if q3 == "Ask for 24 hours to decide, and come back to check the AC and ceiling yourself":
        st.success(
            "Good instinct. The pressure to decide immediately is a classic tactic — "
            "legitimate landlords will give you time to think. Coming back lets you verify "
            "the ceiling stain (musty smell + water stain often means active mold) and test "
            "the AC properly. If the landlord refuses to give you 24 hours, that's your answer."
        )
    elif q3 == "Walk away — the combination of signs here is too risky":
        st.success(
            "Also a valid call. Musty smell + ceiling stain + broken AC + pressure to decide "
            "today is a pattern, not a coincidence. If you do walk, you're not being picky — "
            "you're protecting yourself from a lease that could cost you more than the rent."
        )
    elif q3 == "Sign it — the price is right and Uptown is where you want to be":
        st.error(
            "Price is not enough on its own. The musty smell and ceiling stain together are "
            "a strong mold signal — and mold remediation is the landlord's legal responsibility "
            "but your daily health problem. The artificial urgency ('two other people looking') "
            "is a pressure tactic designed to stop you from thinking clearly."
        )
    elif q3 is not None:
        st.warning(
            "Negotiating the rent is reasonable thinking, but you haven't addressed the bigger "
            "issue — you don't actually know if the AC works or if there's mold behind that "
            "stain. Get that information first before you negotiate anything."
        )

    st.divider()
    st.info("**Quick Check:** What does a water stain on the ceiling usually mean?")

    q4 = st.radio(
        "Water stain meaning:",
        options=[
            "A past leak that was probably fixed",
            "Cosmetic damage from age — common in older buildings",
            "A past or ongoing water issue that needs to be investigated before signing",
            "Normal wear and tear in New Orleans humidity",
        ],
        index=None,
        key="mod2_q2",
    )

    if q4 == "A past or ongoing water issue that needs to be investigated before signing":
        st.success(
            "Correct. A stain doesn't tell you if the problem is fixed. Ask the landlord "
            "directly: 'What caused this and can you show me the repair?' If they can't, "
            "ask for it to be addressed in writing before you sign. Water damage in New Orleans "
            "buildings frequently means mold, which can affect your health and make the unit "
            "legally uninhabitable."
        )
    elif q4 is not None:
        st.error(
            "A stain means water got in — from above, from a pipe, or from the roof. "
            "Whether it's fixed is a separate question you need answered before you sign. "
            "In New Orleans' humidity, untreated water damage almost always means mold. "
            "Always ask what caused it and request proof of repair."
        )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3: DEPOSITS
# ─────────────────────────────────────────────────────────────────────────────

with mod3:
    st.subheader("What are you actually paying when you move in?")
    st.markdown(
        "The sticker price on a listing is never your real move-in cost. "
        "Here's what landlords will ask for — and what you're legally protected from."
    )

    with st.expander("Types of Deposits You'll Encounter", expanded=True):
        st.markdown(
            "**Security Deposit** — Almost always required. Typically equals one month's rent. "
            "In Louisiana, landlords must return it within **one month of move-out** with an "
            "itemized list of any deductions.  \n\n"
            "**First Month's Rent** — Always due at signing.  \n\n"
            "**Last Month's Rent** — Some landlords require this upfront. That means you're "
            "paying three months of rent before you unpack. Budget for this early.  \n\n"
            "**Pet Deposit** — $200–$500 extra if pets are allowed. Sometimes non-refundable.  \n\n"
            "**Application Fee** — $25–$75 for a background/credit check. Non-refundable."
        )

    with st.expander("How to Protect Your Deposit"):
        st.markdown(
            "**Before you move in:**  \n"
            "- Do a walkthrough with your landlord and photograph every scratch, stain, and "
            "dent — timestamped. Email the photos to your landlord the same day so there's "
            "a paper trail.  \n\n"
            "**While you live there:**  \n"
            "- Report maintenance issues in writing (text or email). Never just verbally.  \n"
            "- Pay rent by check or digital transfer — never cash.  \n\n"
            "**When you move out:**  \n"
            "- Request a move-out walkthrough with the landlord present.  \n"
            "- Clean thoroughly — cleaning fees are the #1 deduction.  \n"
            "- If your deposit isn't returned within one month, Louisiana small claims court "
            "allows you to sue for up to $5,000."
        )

    with st.expander("What Can — and Cannot — Be Deducted"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                "**Landlord CAN deduct:**  \n"
                "- Damage you caused (holes, broken fixtures, deep stains)  \n"
                "- Excessive cleaning  \n"
                "- Unpaid rent"
            )
        with col_b:
            st.markdown(
                "**Landlord CANNOT deduct:**  \n"
                "- Normal wear and tear (minor scuffs, faded paint, worn carpet)  \n"
                "- Pre-existing damage you documented at move-in  \n"
                "- Repairs that are their legal responsibility"
            )

    st.divider()
    st.subheader("Scenario Check — Module 3")

    st.info(
        "**Scenario:** You find a 1-bedroom in Mid-City for \\$1,200/month. "
        "The landlord asks for: first month (\\$1,200) + last month (\\$1,200) + "
        "security deposit (\\$1,200) = **\\$3,600 due at signing**. "
        "Is this a reasonable request?"
    )

    q5 = st.radio(
        "Is $3,600 upfront reasonable?",
        options=[
            "No — landlords can only ask for one month upfront",
            "Yes — this is standard and you should expect it",
            "It depends — this is legal, but you should budget for it in advance and get it in writing",
            "No — security deposit can never exceed half a month's rent",
        ],
        index=None,
        key="mod3_q1",
    )

    if q5 == "It depends — this is legal, but you should budget for it in advance and get it in writing":
        st.success(
            "Correct. First + last + security is legal in Louisiana and common in competitive "
            "markets. It just means your true move-in cost is 3x your monthly rent — something "
            "many students don't budget for. Always confirm the exact amounts in the lease "
            "before signing and pay by traceable transfer, not cash."
        )
    elif q5 == "Yes — this is standard and you should expect it":
        st.warning(
            "Partly right — it is legal and does happen. But 'standard' overstates it. "
            "Many landlords only require first month + security (2x rent). "
            "The key is to know this is possible so you can budget accordingly, "
            "and to always get the deposit terms in writing in the lease."
        )
    elif q5 is not None:
        st.error(
            "Louisiana law does not cap how much a landlord can collect upfront. "
            "First + last + security deposit (3x rent) is legal and does happen. "
            "You can try to negotiate, but you need to be prepared for it. "
            "Use the Affordability Calculator to estimate your real move-in costs."
        )

    st.divider()
    st.info(
        "**Quick Check:** You lived in an apartment for 2 years. The carpet looks "
        "worn but isn't stained or torn. Your landlord wants to deduct \\$400 for "
        "'carpet replacement.' Is this allowed?"
    )

    q6 = st.radio(
        "Carpet deduction:",
        options=[
            "Yes — carpet wears out and replacement is expensive",
            "No — normal wear and tear from 2 years of living cannot be deducted",
            "It depends on the lease agreement",
            "Yes, but only if they provide a receipt",
        ],
        index=None,
        key="mod3_q2",
    )

    if q6 == "No — normal wear and tear from 2 years of living cannot be deducted":
        st.success(
            "Correct. Worn carpet from normal use over two years is considered wear and tear — "
            "it is NOT a deductible damage. Landlords can only deduct for damage beyond "
            "normal use (burns, tears, stains you caused). If this happens to you, dispute "
            "it in writing and reference Louisiana Civil Code Article 2693."
        )
    elif q6 is not None:
        st.error(
            "Louisiana law distinguishes between damage and wear and tear. Carpet that's simply "
            "worn down from two years of living is wear and tear — the landlord cannot charge "
            "you for it. Only damage you caused (burns, stains, tears) is deductible. "
            "If they try, you can dispute it — and take them to small claims court if needed."
        )

# ─────────────────────────────────────────────────────────────────────────────
st.divider()

# =============================================================================
# FOOTER
# =============================================================================

st.caption(
    "🏘️ **Housing Training** | "
    "New Orleans Housing Calculator | "
    "© 2026 | Free for student use"
)
