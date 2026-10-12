"""
Dashboard (landing page).

- Average score and accuracy cards
- Recent test performance chart
- Strongest and weakest topics
- A prominent Start practice action
"""

from datetime import date

import altair as alt
import pandas as pd
import streamlit as st

from data.mock_history import (
    ALL_TESTS,
    CORE_TOPIC_MASTERY,
    DASHBOARD_SUMMARY,
    RECENT_TESTS,
    WEAKEST_TOPICS,
)
from data.questions import QUESTIONS_DB
from shared import PRACTICE_PAGE, chart_colors

summary = DASHBOARD_SUMMARY
recent_df = pd.DataFrame(RECENT_TESTS)
recent_df["date"] = pd.to_datetime(recent_df["date"])
all_tests_df = pd.DataFrame(ALL_TESTS)
all_tests_df["date"] = pd.to_datetime(all_tests_df["date"])
colors = chart_colors()

# --- Header -----------------------------------------------------------------
with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
    st.caption(f"{date.today():%A, %d %B %Y} · Target: GATE CS 2027")
    st.badge("Demo dataset", icon=":material/science:", color="secondary")

st.title("Welcome back")
st.markdown(
    f"You're on a **{summary['current_streak_days']}-day study streak** with "
    f"**{summary['total_questions_solved']} questions solved** across {summary['tests_completed']} mock sessions."
)

# --- Start practice call to action ------------------------------------------
with st.container(
    border=True, horizontal=True, vertical_alignment="center", horizontal_alignment="distribute"
):
    with st.container(gap="xsmall"):
        st.markdown("**Ready for today's PYQ practice?**")
        st.caption(
            f"{len(QUESTIONS_DB)} GATE CS Previous Year Questions (2021–2024) · timed · negative marking, "
            "just like the real paper."
        )
    if st.button("Start PYQ Practice", type="primary", icon=":material/play_arrow:", key="start_practice"):
        st.switch_page(PRACTICE_PAGE)

# --- KPI metrics & Topic mastery (Shrunk cards + Topic Mastery) --------------
kpi_col, mastery_col = st.columns([5, 7], gap="medium")

with kpi_col:
    # Row 1: Average score and overall accuracy (shrunk cards, no sparklines)
    r1_c1, r1_c2 = st.columns(2)
    with r1_c1:
        st.metric(
            "Average mock score",
            f"{summary['avg_score']} / 100",
            summary["score_delta"],
            delta_description=summary["score_delta_note"],
            border=True,
        )
    with r1_c2:
        st.metric(
            "Overall accuracy",
            f"{summary['avg_accuracy']}%",
            summary["accuracy_delta"],
            delta_description=summary["accuracy_delta_note"],
            border=True,
        )

    # Row 2: Tests completed and questions solved
    r2_c1, r2_c2 = st.columns(2)
    with r2_c1:
        st.metric(
            "Tests completed",
            summary["tests_completed"],
            f"{summary['total_questions_solved']} questions solved",
            delta_color="off",
            delta_arrow="off",
            border=True,
        )
    with r2_c2:
        st.metric(
            "Questions solved",
            summary["total_questions_solved"],
            f"{summary['current_streak_days']}-day active streak",
            delta_arrow="off",
            border=True,
        )

with mastery_col.container(border=True, height="stretch"):
    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        st.markdown("**Core topic performance**")
        st.caption("Key subjects (OS, DBMS, CN, Algorithms)")

    STATUS_COLORS = {
        "Strong": "green",
        "Moderate": "orange",
        "Needs Work": "red",
    }

    for item in CORE_TOPIC_MASTERY:
        with st.container(gap="xsmall"):
            with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
                st.markdown(f"**{item['topic']}**")
                st.badge(item["status"], color=STATUS_COLORS.get(item["status"], "gray"))
            st.progress(
                item["accuracy"] / 100,
                text=f"{item['accuracy']}% accuracy · {item['attempted']} Qs attempted",
            )

# --- Recent test performance & Priority weak topics ------------------------
chart_col, weak_col = st.columns([7, 5], gap="medium")

with chart_col.container(border=True, height="stretch"):
    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        st.markdown("**Recent test performance**")
        st.caption("Dashed line: 70-mark target benchmark")

    long = recent_df.melt(
        id_vars=["date", "test_name"],
        value_vars=["score", "accuracy"],
        var_name="series",
        value_name="value",
    )
    long["series"] = long["series"].map({"score": "Score", "accuracy": "Accuracy (%)"})

    base = alt.Chart(long).encode(
        x=alt.X("date:T", title=None, axis=alt.Axis(format="%d %b", tickCount=7)),
        y=alt.Y("value:Q", title=None, scale=alt.Scale(domain=[45, 100])),
        color=alt.Color(
            "series:N",
            title=None,
            scale=alt.Scale(domain=["Score", "Accuracy (%)"], range=[colors["primary"], colors["accent"]]),
            legend=alt.Legend(orient="bottom"),
        ),
        tooltip=[
            alt.Tooltip("test_name:N", title="Test"),
            alt.Tooltip("date:T", title="Date", format="%d %b %Y"),
            alt.Tooltip("series:N", title="Metric"),
            alt.Tooltip("value:Q", title="Value", format=".1f"),
        ],
    )
    lines = base.mark_line(strokeWidth=2.5, interpolate="monotone")
    points = base.mark_point(filled=True, size=50)
    cutoff = (
        alt.Chart(pd.DataFrame({"y": [70]}))
        .mark_rule(strokeDash=[6, 4], color=colors["muted"])
        .encode(y="y:Q")
    )
    st.altair_chart(
        (cutoff + lines + points).properties(height=210),
        alt="Mock score progression across recent tests reaching 76.5, surpassing the 70-mark benchmark",
    )

with weak_col.container(border=True, height="stretch"):
    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        st.markdown("**Weak topics (Needs attention)**")
        st.caption("Negative marking audit")

    for t in WEAKEST_TOPICS:
        with st.container(gap="xsmall"):
            with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
                st.markdown(f"**{t['topic']}**")
                st.badge(t["badge"], color="red")
            st.progress(
                t["accuracy"] / 100,
                text=f"{t['accuracy']}% accuracy · :red[−{t['negative_marks_lost']} marks/test]",
            )
            st.caption(t["primary_issue"])

    if st.button("Practice weak topics", icon=":material/tune:", key="dash_practice_weak", width="stretch"):
        st.session_state.practice_topic = "Theory of Computation"
        st.session_state.practice_q_idx = 0
        st.session_state.pop("w_practice_topic", None)
        st.switch_page(PRACTICE_PAGE)

# --- Detailed test log ------------------------------------------------------
with st.expander("Full test history log (14 demo sessions)", icon=":material/table_rows:"):
    st.caption(
        "Demonstration dataset calibrated for GATE CS 2027 preparation. "
        "Averages: Score = 68.5 / 100, Accuracy = 76.8%, Total questions solved = 860 across 14 sessions."
    )
    st.dataframe(
        all_tests_df[["test_name", "date", "questions_count", "score", "accuracy", "time_taken_min"]],
        hide_index=True,
        column_config={
            "test_name": st.column_config.TextColumn("Test"),
            "date": st.column_config.DateColumn("Date", format="D MMM YYYY"),
            "questions_count": st.column_config.NumberColumn("Questions", format="%d Qs"),
            "score": st.column_config.NumberColumn("Score", format="%.1f / 100"),
            "accuracy": st.column_config.ProgressColumn("Accuracy", min_value=0, max_value=100, format="%.1f%%"),
            "time_taken_min": st.column_config.NumberColumn("Time", format="%d min"),
        },
        alt="All 14 mock tests with questions count, score, accuracy, and time taken",
    )
