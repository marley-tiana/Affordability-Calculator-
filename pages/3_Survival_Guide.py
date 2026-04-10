import streamlit as st
import os
import pandas as pd

st.set_page_config(
    page_title="60-Day Survival Guide",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

GROCERY_COMPARISON = {
    "Expensive Stores": {
        "stores": ["Whole Foods", "Rouses", "Robert's Market"],
        "biweekly_cart_cost": 150,
        "description": "Only for emergencies or specific items.",
    },
    "Budget Stores": {
        "stores": ["Walmart", "Trader Joe's", "Costco", "Aldi"],
        "biweekly_cart_cost": 80,
        "description": "Best for majority of food/supplies shopping.",
    },
    "Local Markets": {
        "stores": ["Hong Kong Market", "International Markets"],
        "biweekly_cart_cost": 90,
        "description": "Best for fresh produce, spices, and international brands.",
    }
}

UBER_AVG_COST = 15
JAZZY_PASS_MONTHLY = 45  # RTA 31-day unlimited pass

st.title("The 60-Day Survival Guide")
st.markdown("*Your roadmap to living well in New Orleans on a student budget*")

st.success("Learn how to save hundreds of dollars during your first 60 days in New Orleans!")

st.divider()

# calculate potential savings to show upfront
# note: these are lifestyle tips — separate from the calculator's housing + transport costs
expensive_cost = GROCERY_COMPARISON["Expensive Stores"]["biweekly_cart_cost"]
budget_cost = GROCERY_COMPARISON["Budget Stores"]["biweekly_cart_cost"]
grocery_savings_monthly = (expensive_cost - budget_cost) * 2  # $140/mo

# transport savings: Uber 2x/week (~$129/mo) vs Jazzy Pass ($45/mo)
uber_2x_weekly = UBER_AVG_COST * 2 * 4.3  # ~$129/mo (2 rides/week, ~$4/day)
transport_savings_monthly = uber_2x_weekly - JAZZY_PASS_MONTHLY  # ~$84/mo

furniture_savings = 300  # one-time secondhand vs new

st.header("Your Potential Savings")

total_60day_savings = (grocery_savings_monthly + transport_savings_monthly) * 2 + furniture_savings

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Grocery Savings (60 days)",
        value=f"${grocery_savings_monthly * 2:.0f}",
        help="Shopping at Walmart/Aldi vs Whole Foods/Rouses over 2 months"
    )

with col2:
    st.metric(
        label="Transport Savings (60 days)",
        value=f"${transport_savings_monthly * 2:.0f}",
        help="Jazzy Pass (\$45/mo) vs Uber 2x/week (~\$129/mo) over 2 months"
    )

with col3:
    st.metric(
        label="Furniture Savings",
        value=f"${furniture_savings:.0f}",
        help="One-time savings from buying secondhand vs new"
    )

st.info(
    f"**Total potential lifestyle savings: ${total_60day_savings:.0f} in 60 days.** "
    "These are separate from your housing costs — they cover smarter grocery shopping, "
    "transportation choices, and furnishing your apartment."
)

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Groceries", "Transportation", "Furniture", "Arrival Day", "More Tips"])

with tab1:
    st.header("Smart Grocery Shopping")
    st.subheader("Not All Stores Are Created Equal")

    grocery_data = []
    for category, data in GROCERY_COMPARISON.items():
        grocery_data.append({
            "Category": category,
            "Stores": ", ".join(data["stores"]),
            "Bi-Weekly Cost": f"${data['biweekly_cart_cost']}",
            "Monthly Cost": f"${data['biweekly_cart_cost'] * 2}",
            "Best For": data["description"]
        })
    df_grocery = pd.DataFrame(grocery_data)
    st.dataframe(df_grocery, hide_index=True, use_container_width=True)

    st.success(
        f"**Shopping Smart Saves**: ${grocery_savings_monthly:.0f}/month by choosing budget stores!",
        icon="✨"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Budget-Friendly Stores")
        st.markdown("""
        **Walmart**
        - Best for: Bulk items, household goods
        - Location: Multiple locations
        - Tip: Use Walmart+ for delivery

        **Trader Joe's**
        - Best for: Prepared meals, snacks
        - Location: Uptown
        - Tip: Try their frozen meals ($3-5)

        **Aldi**
        - Best for: Fresh produce, basics
        - Location: Multiple locations
        - Tip: Bring reusable bags (or buy for $0.10)

        **Costco**
        - Best for: Bulk buying with roommates
        - Requires: Membership ($65/year)
        - Tip: Split membership with roommates
        """)

    with col2:
        st.subheader("Shopping Strategies")
        st.markdown("""
        **Weekly Meal Planning**
        - Plan meals before shopping
        - Make a list and stick to it
        - Buy generic/store brands (save 30%)

        **Smart Shopping Times**
        - Check clearance sections
        - Use store apps for digital coupons

        **Bulk Buying Tips**
        - Split Costco runs with roommates
        - Buy non-perishables in bulk

        **Money-Saving Hacks**
        - Cook in batches and freeze
        - Buy produce in season
        - Skip pre-cut vegetables (3x more expensive)
        - Bring your own bags
        """)

    st.markdown("---")

with tab2:
    st.header("Getting Around Smart")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Free and Cheap Options")

        st.markdown("""
        **Tulane Shuttle (FREE)**
        - Grocery shuttle route
        - Campus routes
        - Weekend service
        - Download: TransLoc app
        - [View Shuttle Schedule](https://shuttles.tulane.edu/)

        **Walking/Biking (FREE)**
        - Most of Uptown is walkable
        - Bike lanes on Broadway
        - Free bike parking on campus

        **Streetcar ($1.25/ride)**
        - St. Charles line to Downtown
        - Canal line to French Quarter
        - Jazzy Pass: $45/month unlimited (RTA)
        - Great for weekend exploration
        """)

    with col2:
        st.subheader("Expensive Options")

        st.markdown("""
        **Uber/Lyft**
        - Rush hour pricing (5-7pm): Can double!
        - Surge pricing on weekends
        - Regular Uber usage can be expensive
        - **Use sparingly!**

        **Cost Comparison (per month):**
        - Free shuttle: $0
        - Streetcar (Jazzy Pass): $45
        - Bus + occasional Uber (better than total Uber usage)
        """)

    st.warning(
        f"**Reality Check**: Using Uber just 2x/week costs ~**\\${uber_2x_weekly:.0f}/month** vs a Jazzy Pass at **\\${JAZZY_PASS_MONTHLY}/month**. "
        f"That's **\\${transport_savings_monthly:.0f}/month** in savings!",
        icon="💸"
    )

    st.markdown("---")

    st.subheader("Smart Transportation Strategy")

    st.markdown("""
    **For Groceries:**
    - Use Tulane shuttle grocery line
    - Walk to Whole Foods (25-30 min walk from campus)


    **For Class:**
    - Walk or bike (free exercise!)
    - Use campus shuttles
    - Avoid Uber for daily commute

    **For Errands & Exploring:**
    - Take streetcar to downtown ($1.25)
    - Plan trips to combine errands

    **Emergency Fund:**
    - Keep $50/month for emergency Ubers
    - Late night safety rides
    - Medical emergencies
    """)

with tab3:
    st.header("Furnish Smart, Not Hard")
    st.subheader("Rule #1: Never Buy New Furniture as a Student!")

    st.success(
        f"**Save ${furniture_savings}** by furnishing your entire place secondhand!",
        icon="♻️"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Where to Find Free/Cheap Stuff")

        st.markdown("""
        **1. Tulane Facebook Groups**
        - Tulane Classifieds
        - Tulane Housing & Roommates
        - Graduating students sell cheap!

        **2. Online Marketplaces**
        - Facebook Marketplace
        - Craigslist New Orleans
        - OfferUp
        - Nextdoor

        **3. University Programs**
        - Tulane ReUse Wave (move-out donations)
        - End-of-semester giveaways
        - RA bulletin boards

        **4. Curb Shopping**
        - Check apartment complexes Thursday-Sunday
        - Move-out seasons: May/June & December
        - Uptown/University area
        - **Always inspect for bed bugs!**
        """)

    with col2:
        st.subheader("Best Times to Hunt")

        st.markdown("""
        **Peak Seasons:**
        - **May/June** (end of spring semester)
          - Graduating seniors leaving
          - International students returning home
          - Summer subleasers moving out

        - **December** (end of fall semester)
          - Fall graduates leaving
          - Study abroad students departing

        **Strategy:**
        - Start looking 2 weeks before move-in
        - Check daily during peak season
        - Move fast on good deals
        - Bring truck/SUV for pickup
        - Go with a friend (safety + help)
        """)

    st.markdown("---")

    st.subheader("Essential First-Apartment Shopping List")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Bedroom**
        - [ ] Bed frame
        - [ ] Mattress
        - [ ] Sheets
        - [ ] Pillow
        - [ ] Lamp
        - [ ] Hangers
        """)

    with col2:
        st.markdown("""
        **Living Room**
        - [ ] Couch
        - [ ] Coffee table
        - [ ] TV stand
        - [ ] Rug
        - [ ] Lamp
        """)

    with col3:
        st.markdown("""
        **Kitchen**
        - [ ] Pots & pans
        - [ ] Dishes
        - [ ] Utensils
        - [ ] Trash can
        - [ ] Dish towels
        """)

with tab4:
    st.header("Arrival Day")
    st.markdown(
        "Louis Armstrong New Orleans International Airport (MSY) is about 12 miles "
        "from campus. Here's exactly how to get to your housing on day one."
    )

    with st.expander("Your Options from MSY", expanded=True):
        st.markdown(
            "| Option | Cost | Time | Best For |\n"
            "|---|---|---|---|\n"
            "| **Uber / Lyft** | \\$30–\\$50 | 20–35 min | Most students — easiest with luggage |\n"
            "| **Airport Shuttle (Airport Shuttle NOLA)** | \\$24/person | 25–45 min | Budget travelers, shared van |\n"
            "| **RTA Bus (Route 202 + transfer)** | \\$1.25 | 90+ min | Light packing only, very slow |\n"
            "| **Taxi** | \\$36 flat rate to downtown | 20–35 min | Fixed price, no surge — useful during events |\n"
        )

    with st.expander("How to Install & Set Up Uber and Lyft — Step by Step", expanded=True):
        st.markdown("**Do this before you travel — not at the airport.**")
        st.markdown(" ")

        def step_image(path, caption):
            if os.path.exists(path):
                st.image(path, caption=caption, use_container_width=True)

        st.subheader("Uber")

        st.markdown("**Step 1 — Download the app**")
        st.markdown("Open the **App Store** (iPhone) or **Google Play** (Android). Search for **Uber** and tap Install. The app is free.")
        step_image("images/tutorial/uber_step1.jpg", "Search 'Uber' in the App Store or Google Play")

        st.markdown(" ")
        st.markdown("**Step 2 — Create your account**")
        st.markdown("Open the app and tap **Sign Up**. Enter your name, email address, and phone number. Uber will text you a 4-digit verification code — enter it to confirm your number.")
        step_image("images/tutorial/uber_step2.jpg", "Uber sign-up screen — enter your email and phone number")

        st.markdown(" ")
        st.markdown("**Step 3 — Add a payment method**")
        st.markdown("Tap **Payment** in the menu and select **Add Payment Method**. Enter your credit or debit card number. International cards are accepted. You can also link PayPal.")
        step_image("images/tutorial/uber_step3.jpg", "Uber payment screen — Add Credit or Debit Card")

        st.markdown(" ")
        st.markdown("**Step 4 — You're ready**")
        st.markdown("The home screen shows a map with a **Where to?** bar. Tap it, enter your destination, choose your ride type, and confirm. You'll see the driver's name, photo, license plate, and ETA.")
        step_image("images/tutorial/uber_step4.jpg", "Uber home screen showing 'Where to?' search bar")

        st.divider()

        st.subheader("Lyft")

        st.markdown("**Step 1 — Download the app**")
        st.markdown("Search **Lyft** in the App Store or Google Play and tap Install. The app is free.")
        step_image("images/tutorial/lyft_step1.jpg", "Search 'Lyft' in the App Store or Google Play")

        st.markdown(" ")
        st.markdown("**Step 2 — Sign up with your phone number**")
        st.markdown("Open the app and tap **Create an account**. Enter your phone number — Lyft will text you a 6-digit code. Enter it, then fill in your name and email.")
        step_image("images/tutorial/lyft_step2.jpg", "Lyft sign-up screen — enter your phone number")

        st.markdown(" ")
        st.markdown("**Step 3 — Add a payment method**")
        st.markdown("Tap the menu (top left) → **Payment** → **Add a card**. Enter your card details. International cards work fine.")
        step_image("images/tutorial/lyft_step3.jpg", "Lyft payment screen — Add a card")

        st.markdown(" ")
        st.markdown("**Step 4 — You're ready**")
        st.markdown("Tap **Where are you going?**, enter your destination, select a ride type, and confirm. Lyft shows the driver's name, photo, plate, and ETA just like Uber.")
        step_image("images/tutorial/lyft_step4.jpg", "Lyft home screen showing 'Where are you going?' bar")

        st.divider()
        st.info(
            "**Tip:** Install both apps before you travel. Prices and wait times vary — "
            "checking both takes 10 seconds and can save you money, especially at the airport."
        )

    with st.expander("Rideshare Tips for Arrival Day"):
        st.markdown(
            "**Before you land:**  \n"
            "- Make sure your Uber or Lyft app is installed and your payment method is set up "
            "before you board your flight. Airport Wi-Fi is unreliable for setting up accounts.  \n\n"
            "**At the airport:**  \n"
            "- Rideshare pickup is on **Level 1 of the Ground Transportation Center** — "
            "follow signs for 'Rideshare.' It is NOT at the main arrivals curb.  \n"
            "- Always confirm the license plate in your app before getting in.  \n\n"
            "**Surge pricing:**  \n"
            "- If there's a major event in New Orleans, surge pricing can push fares to \\$80+. "
            "If that happens, wait 20–30 minutes inside the terminal or take the flat-rate taxi.  \n\n"
            "**With a lot of luggage:**  \n"
            "- Request an **XL** or **Comfort** vehicle if you have more than two large bags."
        )

    with st.expander("If You're Coming from Internationally"):
        st.markdown(
            "**Get through customs first, then request your ride.** "
            "Do not request a rideshare while still in the customs/immigration line.  \n\n"
            "**Currency:** Carry some cash (\\$20–\\$40) for emergencies — not all smaller "
            "shops or taxis accept international cards reliably on the first swipe.  \n\n"
            "**Phone signal:** Connect to airport Wi-Fi to request your ride if you don't have a US data plan yet."
        )

    st.divider()
    st.subheader("Getting a SIM card / US phone plan")

    with st.expander("Best Budget Carriers", expanded=True):
        st.markdown(
            "| Carrier | Plan | Cost/mo | Network | Notes |\n"
            "|---|---|---|---|---|\n"
            "| **Mint Mobile** | 5GB | \\$15 | T-Mobile | Buy online, SIM mailed — order before you travel |\n"
            "| **AT&T Prepaid** | 5GB | \\$30 | AT&T | Walk-in store, solid coverage uptown |\n"
            "| **Visible** | Unlimited | \\$25 | Verizon | Good coverage in New Orleans, app-based |\n"
            "| **T-Mobile Prepaid** | Unlimited | \\$40 | T-Mobile | Walk-in store, activated same day |\n"
            "| **Google Fi** | Flexible | \\$20+ | Multi-network | Best if you travel internationally often |\n\n"
            "T-Mobile and AT&T have stores on Magazine Street and St. Charles Avenue near campus."
        )

    with st.expander("eSIM vs. Physical SIM"):
        st.markdown(
            "**eSIM (recommended if your phone supports it):**  \n"
            "- No physical card needed — activate entirely through settings  \n"
            "- Set it up before you even board your flight  \n"
            "- Mint Mobile, Visible, T-Mobile, and AT&T all support eSIM  \n\n"
            "**Physical SIM:**  \n"
            "- Pick up in-store or at a carrier kiosk  \n"
            "- MSY Airport has prepaid SIMs near baggage claim  \n"
            "- Walmart and Walgreens in New Orleans also carry prepaid SIM kits  \n\n"
            "**Check if your phone is unlocked first.** "
            "Check Settings > General > About > Carrier Lock (iPhone) or contact your provider before traveling."
        )

    with st.expander("International Students: Day One Checklist"):
        st.markdown(
            "1. Connect to MSY airport Wi-Fi. Activate eSIM if you ordered one.  \n"
            "2. No SIM yet? Use airport Wi-Fi to request your Uber/Lyft.  \n"
            "3. Within your first day or two: visit a T-Mobile or AT&T store. "
            "Bring your passport and a payment method. No SSN needed for prepaid.  \n"
            "4. Avoid airport carrier kiosks for your primary plan — walk-in stores have better options.  \n"
            "5. Keep WhatsApp / iMessage as backup communication over Wi-Fi while you set up a local number."
        )


with tab5:
    st.header("More Money-Saving Tips")

    st.subheader("Utilities & Services")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Internet & Phone**
        - Split internet with roommates
        - Use family phone plan if possible
        - Student discounts: AT&T, Verizon, T-Mobile
        - Consider prepaid plans

        **Electricity & Gas**
        - Entergy New Orleans is main provider
        - Budget billing = same amount each month
        - Turn off AC when not home (save 10-15%)
        """)

    with col2:
        st.markdown("""
        **Entertainment**
        - Tulane gym membership (FREE with tuition!)
        - Free campus events (movies, concerts)
        - Student discounts at museums
        - Free festivals (French Quarter Fest)
        - Library card = free books, movies, music

        **Food Delivery**
        - Use student discounts (UberEats, DoorDash)
        - Pick up instead of delivery
        - Share delivery fees with roommates
        - Cook at home = save $200-400/month
        """)

    st.markdown("---")

    st.subheader("Student Discounts in New Orleans")

    st.markdown("""
    **With Tulane ID:**
    - Audubon Zoo & Aquarium: Student pricing
    - WWII Museum: Student discount
    - Movie theaters: $2-3 off tickets
    - Restaurants: Ask! Many offer 10-15% off
    - Spotify + Hulu bundle: \$4.99/month (normally \$18)
    - Amazon Prime Student: 6 months free, then $7.49/month

    **Apps to Download:**
    - UNiDAYS: Student verification for discounts
    - Student Beans: More student discounts
    - Honey: Automatic coupon finder
    - Rakuten: Cash back on purchases
    """)

    st.markdown("---")

    st.subheader("Part-Time Work Opportunities")

    st.warning(
        "🌍 **International Students (F-1 visa):** You are only authorized to work **on-campus**. "
        "Working off-campus without authorization is a visa violation. "
        "For more information contact the Office of International Students and Scholars at oiss@tulane.edu"
    )

    st.markdown("""
    **On-Campus Jobs**
    - Library desk attendant
    - Campus tour guide
    - Research assistant
    - Tutor

    **Off-Campus Jobs** *(domestic students only, unless authorized)*
    - Restaurant server
    - Barista
    - Retail
    - Babysitting/tutoring
    - Internships

    **Work-Study**: Check if you qualify for federal work-study program
    """)

st.divider()

st.header("Your Action Plan")

with st.container(border=True):
    st.subheader(f"Follow This Plan to Save ${total_60day_savings:.0f} in Your First 60 Days")

    st.markdown("""
**Week 1 - Before Arrival:**
- Join Tulane Facebook groups
- Research apartments on your shuttle route
- Make furniture wishlist

**Week 2 - First Week in NOLA:**
- Download TransLoc (shuttle) app
- Get Jazzy Pass for streetcar ($45/month)
- Scout furniture from graduating students

**Weeks 3-4 - Settling In:**
- Shop at Walmart/Aldi for groceries
- Set up utilities with roommates
- Learn shuttle routes

**Weeks 5-8 - Optimize:**
- Meal prep on Sundays
- Use shuttle instead of Uber
- Apply student discounts everywhere
    """)

st.divider()

# personalized tips if the user has already run the calculator
if st.session_state.get("calculation_results"):
    results = st.session_state.calculation_results
    day60 = results["day60"]
    inp = results.get("inputs", {})
    transport_mode = inp.get("transport_mode", "")
    transport_cost_user = inp.get("transport", 0)

    # only show transport savings if the user picked an expensive option
    personalized_transport_savings = 0
    if transport_mode == "Uber / Lyft" and transport_cost_user > (JAZZY_PASS_MONTHLY * 2):
        personalized_transport_savings = transport_cost_user - (JAZZY_PASS_MONTHLY * 2)

    st.success(
        f"**Your 60-Day Housing Cost**: **${day60:,.2f}** (from Calculator)\n\n"
        f"**On top of that, these lifestyle tips can save you:**\n"
        f"- Grocery savings: **${grocery_savings_monthly * 2:.0f}** (budget vs expensive stores)\n"
        + (f"- Transport savings: **${personalized_transport_savings:.0f}** (switching to Jazzy Pass)\n" if personalized_transport_savings > 0 else "")
        + f"- Furniture savings: **${furniture_savings}** (secondhand vs new)\n\n"
        f"These savings are *in addition* to your housing budget — they cover groceries, "
        f"furniture, and daily spending."
    )
else:
    st.info("**Tip**: Use the Calculator to estimate your 60-day housing costs, then come back here for savings tips!")

st.markdown("---")
st.caption("Updated for 2026 | Based on real student experiences. Have more tips? Share with future students!")
