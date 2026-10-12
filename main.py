"""
Competitive Exam Analyzer - Main Streamlit Application Entrypoint.
A frontend platform for competitive exam analysis (GATE CS), timed practice,
and diagnostic recommendations.

Look and feel come from `.streamlit/config.toml` (native theming), and the
three views live in `app_pages/` and are wired up with `st.navigation`.
"""

import streamlit as st

from shared import ANALYSIS_PAGE, DASHBOARD_PAGE, PRACTICE_PAGE, init_state, reset_practice

st.set_page_config(
    page_title="Prepmaster · GATE CS analyzer",
    page_icon=":material/school:",
    layout="wide",
)

init_state()

page = st.navigation(
    [
        st.Page(DASHBOARD_PAGE, title="Dashboard", icon=":material/space_dashboard:", default=True),
        st.Page(PRACTICE_PAGE, title="Practice", icon=":material/edit_note:"),
        st.Page(ANALYSIS_PAGE, title="Analysis", icon=":material/insights:"),
    ],
    position="top",
)

# Sidebar: app identity, aspirant profile, and a global reset.
with st.sidebar:
    st.header("Prepmaster")
    st.caption("Competitive exam analyzer")

    with st.container(border=True):
        st.markdown("**Aspirant profile**")
        st.markdown(":gray[Target exam]  \nGATE CS 2027 *(Feb 2027)*")
        st.markdown(":gray[Target score]  \n:green[**75+ marks**]")
        st.markdown(":gray[Study track]  \nCore CS + engineering math")
        st.caption(":material/science: Demo dataset · 14 sessions")

    st.button(
        "Reset practice session",
        icon=":material/restart_alt:",
        help="Clear answers and restart the current practice test",
        on_click=reset_practice,
        width="stretch",
    )

page.run()
