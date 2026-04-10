"""Navigation component for the multi-page app."""
import streamlit as st


def get_page_config():
    """All pages with their icons and file paths."""
    return {
        "Home": {
            "icon": "🏠",
            "file": "Home.py",
            "description": "Welcome & Overview"
        },
        "Calculator": {
            "icon": "🧮",
            "file": "pages/1_Calculator.py",
            "description": "Affordability Calculator"
        },
        "My Results": {
            "icon": "📊",
            "file": "pages/2_My_Results.py",
            "description": "Saved Calculations"
        },
        "Survival Guide": {
            "icon": "📚",
            "file": "pages/3_Survival_Guide.py",
            "description": "Money-Saving Tips"
        },
        "Cost Analysis": {
            "icon": "💰",
            "file": "pages/4_Cost_Analysis.py",
            "description": "Compare Scenarios"
        },
        "Fare Estimator": {
            "icon": "🚕",
            "file": "pages/5_Fare_Estimator.py",
            "description": "Ride Cost Calculator"
        },
        "Student Advice": {
            "icon": "💬",
            "file": "pages/7_Student_Advice.py",
            "description": "Tips from Students"
        },
        "Housing Guide": {
            "icon": "🏘️",
            "file": "pages/9_Housing_Guide.py",
            "description": "Find & Secure Housing"
        },
        "Help": {
            "icon": "ℹ️",
            "file": "pages/6_Help.py",
            "description": "Help & FAQs"
        }
    }


def render_top_navigation():
    """Render the nav bar at the top of every page."""
    pages = get_page_config()

    cols = st.columns(len(pages))
    for idx, (page_name, page_info) in enumerate(pages.items()):
        with cols[idx]:
            if st.button(
                f"{page_info['icon']} {page_name}",
                key=f"nav_{page_name}",
                use_container_width=True,
                help=page_info['description']
            ):
                st.switch_page(page_info['file'])

    st.divider()
