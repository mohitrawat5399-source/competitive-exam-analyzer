"""
Competitive Exam Analyzer - Main Streamlit Application Entrypoint.
A modern frontend platform for competitive exam analysis (GATE CS), timed practice,
and diagnostic recommendations.
"""

import streamlit as st
from styles import CUSTOM_CSS
from components.dashboard_view import render_dashboard
from components.practice_view import render_practice
from components.analysis_view import render_analysis

# 1. Page Configuration
st.set_page_config(
    page_title="GATE CS Exam Analyzer & Practice Suite",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom Theme Styles
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 3. Session State Initialization for Navigation
if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = "Dashboard"

# 4. Sidebar Navigation & Candidate Info
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.8rem;">🎯</span>
                <div>
                    <div style="font-weight: 800; font-size: 1.15rem; color: #f8fafc; line-height: 1.2;">
                        PrepMaster
                    </div>
                    <div style="font-size: 0.78rem; color: #818cf8; font-weight: 600; text-transform: uppercase;">
                        Competitive Exam Analyzer
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Navigation Radio
    nav_options = ["Dashboard", "Practice", "Analysis"]
    nav_icons = {
        "Dashboard": "📊 Dashboard",
        "Practice": "✍️ Practice Arena",
        "Analysis": "📈 Analysis & Diagnostics"
    }

    # Ensure valid selected index
    current_index = nav_options.index(st.session_state["nav_selection"]) if st.session_state["nav_selection"] in nav_options else 0

    selected_page = st.radio(
        "Navigation",
        options=nav_options,
        index=current_index,
        format_func=lambda x: nav_icons[x],
        key="sidebar_nav_radio"
    )

    # Sync state if user clicked sidebar radio
    if selected_page != st.session_state["nav_selection"]:
        st.session_state["nav_selection"] = selected_page
        st.rerun()

    st.markdown("---")

    # Candidate Profile & Target Card
    st.markdown("#### 👤 Aspirant Profile")
    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 10px; padding: 14px; font-size: 0.85rem;">
            <div style="color: #94a3b8; margin-bottom: 4px;">Target Exam:</div>
            <div style="color: #f8fafc; font-weight: 700; margin-bottom: 8px;">GATE CS & IT 2025/2026</div>

            <div style="color: #94a3b8; margin-bottom: 4px;">Target Score:</div>
            <div style="color: #34d399; font-weight: 700; margin-bottom: 8px;">75+ Marks (Top IITs)</div>

            <div style="color: #94a3b8; margin-bottom: 4px;">Study Track:</div>
            <div style="color: #cbd5e1; font-weight: 500;">Core CS + Engineering Math</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Session Reset Utility
    if st.button("🔄 Reset Practice Session", use_container_width=True, help="Clear answers and restart current practice test"):
        st.session_state["user_answers"] = {}
        st.session_state["marked_for_review"] = set()
        st.session_state["test_submitted"] = False
        st.session_state["practice_q_idx"] = 0
        st.success("Session reset!")
        st.rerun()

# 5. Route to Selected View
active_page = st.session_state["nav_selection"]

if active_page == "Dashboard":
    render_dashboard()
elif active_page == "Practice":
    render_practice()
elif active_page == "Analysis":
    render_analysis()
