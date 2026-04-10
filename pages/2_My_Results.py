import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="My Saved Results",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)


def load_saved_results():
    """Load saved results from session state."""
    if "saved_results" not in st.session_state:
        st.session_state.saved_results = []
    return st.session_state.saved_results


def save_current_result():
    """Save the current calculation result."""
    if not st.session_state.get("calculation_results"):
        return False

    results = st.session_state.calculation_results

    result_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().strftime("%B %d, %Y"),
        "time": datetime.now().strftime("%I:%M %p"),
        "day0": results["day0"],
        "day60": results["day60"],
        "remaining": results["remaining"],
        "breakdown": results["breakdown"],
        "inputs": results["inputs"]
    }

    # add to saved results, newest first
    if "saved_results" not in st.session_state:
        st.session_state.saved_results = []

    st.session_state.saved_results.insert(0, result_entry)
    return True


def clear_all_results():
    """Clear all saved results."""
    st.session_state.saved_results = []
    st.session_state.confirm_clear = False


def get_risk_label(remaining, day60):
    """Get risk level text label."""
    if remaining < 0:
        return "High Risk"
    elif remaining < 0.1 * day60:
        return "Low Buffer"
    elif remaining < 0.2 * day60:
        return "Moderate"
    else:
        return "Good"


def show_risk_badge(remaining, day60):
    """Display risk level using native Streamlit components."""
    label = get_risk_label(remaining, day60)
    if label == "High Risk":
        st.error(f"Risk Level: {label}")
    elif label == "Low Buffer":
        st.warning(f"Risk Level: {label}")
    elif label == "Moderate":
        st.info(f"Risk Level: {label}")
    else:
        st.success(f"Risk Level: {label}")


st.title("My Saved Results")
st.markdown("View and manage your calculation history")

st.divider()

# show current calc if there is one to save
if st.session_state.get("calculation_results"):
    results = st.session_state.calculation_results
    inputs = results["inputs"]

    st.header("Current Calculation")

    st.info("You have a new calculation! Save it to keep it in your history.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Move-in Cost", f"${results['day0']:,.2f}")

    with col2:
        st.metric("60-Day Total", f"${results['day60']:,.2f}")

    with col3:
        remaining_pct = (results['remaining'] / inputs['savings'] * 100) if inputs['savings'] > 0 else 0
        st.metric("Balance After", f"${results['remaining']:,.2f}",
                 delta=f"{remaining_pct:.1f}% remaining")

    show_risk_badge(results['remaining'], results['day60'])

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Save This Result", use_container_width=True, type="primary"):
            if save_current_result():
                st.success("Result saved successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("Failed to save result")

    with st.expander("View Input Details"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
**Housing:**
- Rent: ${inputs['rent']:,.2f}
- Deposit: ${inputs['deposit']:,.2f}
- Application Fee: ${inputs['application']:,.2f}
- Admin Fee: ${inputs['admin']:,.2f}
""")

        with col2:
            st.markdown(f"""
**Other:**
- Roommates: {inputs['roommates']}
- Apartment Type: {inputs['unit_type']}
- Transportation: ${inputs['transport']:,.2f}
- Savings: ${inputs['savings']:,.2f}
""")

    st.divider()

else:
    st.info("**No current calculation.** Go to the Calculator page to create one!")
    st.divider()

# saved history
saved_results = load_saved_results()

st.header("Saved Results History")

if saved_results:
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(f"**{len(saved_results)}** saved calculation(s)")

    with col3:
        if st.button("Clear All", use_container_width=True):
            st.session_state.confirm_clear = True

    # confirm before deleting everything
    if st.session_state.get("confirm_clear", False):
        st.warning("**Are you sure you want to delete all saved results?** This cannot be undone!")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("Yes, Delete All", use_container_width=True, type="primary"):
                clear_all_results()
                st.success("All results cleared!")
                st.rerun()

        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.confirm_clear = False
                st.rerun()

    st.divider()

    for idx, result in enumerate(saved_results):
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(f"{result['date']} at {result['time']}")

            with col2:
                show_risk_badge(result['remaining'], result['day60'])

            metric_col1, metric_col2, metric_col3 = st.columns(3)

            with metric_col1:
                st.metric("Move-in", f"${result['day0']:,.2f}")

            with metric_col2:
                st.metric("60-Day Total", f"${result['day60']:,.2f}")

            with metric_col3:
                st.metric("Remaining", f"${result['remaining']:,.2f}")

            with st.expander("View Input Details"):
                inputs = result['inputs']
                d1, d2 = st.columns(2)
                with d1:
                    st.markdown(f"""
**Housing**
- Rent: ${inputs['rent']:,.2f}
- Deposit: ${inputs['deposit']:,.2f}
- Roommates: {inputs['roommates']}
- Unit Type: {inputs['unit_type']}
""")
                with d2:
                    st.markdown(f"""
**Other**
- Transport: ${inputs['transport']:,.2f}
- Mode: {inputs['transport_mode']}
- Savings: ${inputs['savings']:,.2f}
""")

            if st.button(f"Delete", key=f"delete_{idx}"):
                st.session_state.saved_results.pop(idx)
                st.success("Result deleted!")
                st.rerun()

            st.divider()

    st.subheader("Summary Statistics")

    min_60day = min(r['day60'] for r in saved_results)
    max_60day = max(r['day60'] for r in saved_results)

    stat_col1, stat_col2, stat_col3 = st.columns(3)

    with stat_col1:
        st.metric("Lowest 60-Day Cost", f"${min_60day:,.2f}")

    with stat_col2:
        st.metric("Highest 60-Day Cost", f"${max_60day:,.2f}")

    with stat_col3:
        st.metric("Total Calculations", len(saved_results))

else:
    st.info("""
    **No saved results yet.**

    **How to save results:**
    1. Go to the **Calculator** page
    2. Fill out the form and click "Calculate"
    3. Come back to this page
    4. Click "Save This Result"

    Your results will accumulate here for easy comparison!
    """)

st.divider()

st.caption("Results are saved in your browser session. Clear your browser data or close the app to reset.")
