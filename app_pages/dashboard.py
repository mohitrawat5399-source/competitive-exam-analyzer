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

from data.mock_history import DASHBOARD_SUMMARY, RECENT_TESTS, STRONGEST_TOPICS, WEAKEST_TOPICS
from data.questions import QUESTIONS_DB
from shared import PRACTICE_PAGE, chart_colors

summary = DASHBOARD_SUMMARY
tests = pd.DataFrame(RECENT_TESTS)
tests["date"] = pd.to_datetime(tests["date"])
colors = chart_colors()

# --- Header -----------------------------------------------------------------
st.caption(f"{date.today():%A, %d %B} · GATE CS 2026")
st.title("Welcome back")
st.markdown(
    f"You're on a **{summary['current_streak_days']}-day streak**. At this pace you're projected "
    f"to score **{summary['predicted_gate_score']} / 1000**, roughly **{summary['predicted_rank']}**."
)

# --- Start practice call to action ------------------------------------------
with st.container(
    border=True, horizontal=True, vertical_alignment="center", horizontal_alignment="distribute"
):
    with st.container(gap="xsmall"):
        st.markdown("**Ready for today's session?**")
        st.caption(
            f"{len(QUESTIONS_DB)} GATE CS questions from 2021–2024 · timed · negative marking, "
            "just like the real paper."
        )
    if st.button("Start practice", type="primary", icon=":material/play_arrow:", key="start_practice"):
        st.switch_page(PRACTICE_PAGE)

# --- KPI cards --------------------------------------------------------------
with st.container(horizontal=True):
    st.metric(
        "Average mock score",
        f"{summary['avg_score']} / 100",
        summary["score_delta"],
        delta_description=summary["score_delta_note"],
        chart_data=tests["score"].tolist(),
        chart_type="area",
        border=True,
        height="stretch",
    )
    st.metric(
        "Overall accuracy",
        f"{summary['avg_accuracy']}%",
        summary["accuracy_delta"],
        delta_description=summary["accuracy_delta_note"],
        chart_data=tests["accuracy"].tolist(),
        chart_type="area",
        border=True,
        height="stretch",
    )
    st.metric(
        "Tests completed",
        summary["tests_completed"],
        f"{summary['total_questions_solved']} questions solved",
        delta_color="off",
        delta_arrow="off",
        border=True,
        height="stretch",
    )
    st.metric(
        "Predicted percentile",
        f"{summary['estimated_percentile']}",
        f"{summary['current_streak_days']}-day streak",
        delta_arrow="off",
        border=True,
        height="stretch",
    )

# --- Recent test performance ------------------------------------------------
with st.container(border=True):
    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        st.markdown("**Recent test performance**")
        st.caption("Dashed line: ~70-mark cutoff for top IITs")

    long = tests.melt(
        id_vars=["date", "test_name"],
        value_vars=["score", "accuracy"],
        var_name="series",
        value_name="value",
    )
    long["series"] = long["series"].map({"score": "Score", "accuracy": "Accuracy (%)"})

    base = alt.Chart(long).encode(
        x=alt.X("date:T", title=None, axis=alt.Axis(format="%d %b", tickCount=7)),
        y=alt.Y("value:Q", title=None, scale=alt.Scale(domain=[40, 100])),
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
    points = base.mark_point(filled=True, size=60)
    cutoff = (
        alt.Chart(pd.DataFrame({"y": [70]}))
        .mark_rule(strokeDash=[6, 4], color=colors["muted"])
        .encode(y="y:Q")
    )
    st.altair_chart(
        (cutoff + lines + points).properties(height=320),
        alt="Mock score rose from 54 to 76.5 over seven tests, crossing the 70-mark cutoff",
    )

# --- Strongest and weakest topics -------------------------------------------
strong_col, weak_col = st.columns(2)

with strong_col.container(border=True, height="stretch"):
    st.subheader("Strongest topics", icon=":material/trending_up:")
    st.caption("Consistently above 80% accuracy.")
    for t in STRONGEST_TOPICS:
        with st.container(gap="xsmall"):
            with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
                st.markdown(f"**{t['topic']}**")
                st.badge(t["badge"], color="green")
            st.progress(t["accuracy"] / 100, text=f"{t['accuracy']}% accuracy · {t['mastery']}")
            st.caption(t["highlight"])

with weak_col.container(border=True, height="stretch"):
    st.subheader("Needs attention", icon=":material/trending_down:")
    st.caption("Where negative marking is costing you the most.")
    for t in WEAKEST_TOPICS:
        with st.container(gap="xsmall"):
            with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
                st.markdown(f"**{t['topic']}**")
                st.badge(t["badge"], color="red")
            st.progress(
                t["accuracy"] / 100,
                text=f"{t['accuracy']}% accuracy · :red[−{t['negative_marks_lost']} marks lost per test]",
            )
            st.caption(t["primary_issue"])

# --- Detailed log -----------------------------------------------------------
with st.expander("Recent test log", icon=":material/table_rows:"):
    st.dataframe(
        tests[["test_name", "date", "score", "accuracy", "time_taken_min", "rank"]],
        hide_index=True,
        column_config={
            "test_name": st.column_config.TextColumn("Test"),
            "date": st.column_config.DateColumn("Date", format="D MMM YYYY"),
            "score": st.column_config.NumberColumn("Score", format="%.1f / 100"),
            "accuracy": st.column_config.ProgressColumn("Accuracy", min_value=0, max_value=100, format="%.1f%%"),
            "time_taken_min": st.column_config.NumberColumn("Time", format="%d min"),
            "rank": st.column_config.NumberColumn("Est. AIR", format="%d"),
        },
        alt="Recent mock tests with score, accuracy, time taken and estimated rank",
    )
