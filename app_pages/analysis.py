"""
Analysis and diagnostics.

- Sample score and accuracy (uses the latest practice attempt when available)
- Topic mastery chart vs. cutoff benchmark
- Weak-topic list with negative-marking diagnosis
- Recommended topics for revision
"""

import altair as alt
import pandas as pd
import streamlit as st

from data.mock_history import DASHBOARD_SUMMARY, RECOMMENDED_REVISIONS, TOPIC_MASTERY, WEAKEST_TOPICS
from shared import PRACTICE_PAGE, chart_colors

ss = st.session_state
colors = chart_colors()
PRIORITY_STYLE = {
    "High": (":material/priority_high:", "red"),
    "Medium": (":material/schedule:", "orange"),
    "Maintenance": (":material/check:", "green"),
}

# --- Header -----------------------------------------------------------------
st.caption("Analysis")
st.title("Performance diagnostics")
st.markdown("Find the high-yield gaps, see how each subject compares to the cutoff, and follow a focused revision plan.")

latest = ss.latest_test_results
if latest:
    score, max_score = latest["net_score"], latest["max_marks"]
    accuracy = latest["accuracy"]
    correct, incorrect, skipped = latest["correct_count"], latest["incorrect_count"], latest["unattempted_count"]
    source = "Latest practice session"
else:
    score, max_score, accuracy = 76.5, 100, 83.2
    correct, incorrect, skipped = 48, 11, 6
    source = "Full mock 4 (benchmark)"

with st.container(horizontal=True, gap="small", vertical_alignment="center"):
    st.caption("Showing")
    st.badge(source, icon=":material/dataset:", color="gray")

# --- Score and accuracy -----------------------------------------------------
with st.container(horizontal=True):
    st.metric(
        "Score",
        f"{score} / {max_score}",
        f"{score / max_score * 100:.1f}%",
        delta_description="of maximum",
        delta_arrow="off",
        delta_color="off",
        border=True,
    )
    st.metric(
        "Accuracy",
        f"{accuracy}%",
        f"{accuracy - 75:+.1f} pts",
        delta_description="vs 75% target",
        border=True,
    )
    st.metric(
        "Correct · incorrect",
        f"{correct} · {incorrect}",
        f"{skipped} unattempted",
        delta_arrow="off",
        delta_color="off",
        border=True,
    )
    st.metric(
        "Projected rank",
        DASHBOARD_SUMMARY["predicted_rank"],
        f"Top {100 - DASHBOARD_SUMMARY['estimated_percentile']:.1f}%",
        delta_arrow="off",
        border=True,
    )

# --- Topic mastery ----------------------------------------------------------
mastery = pd.DataFrame(TOPIC_MASTERY).sort_values("accuracy", ascending=False)
mastery["tier"] = pd.cut(
    mastery["accuracy"], bins=[0, 65, 80, 101], labels=["Weak", "Moderate", "Strong"], right=False
).astype(str)

with st.container(border=True):
    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        with st.container(gap="xsmall"):
            st.markdown("**Topic mastery vs. cutoff benchmark**")
            st.caption("Bars show your accuracy; the tick marks the target for top IITs / IISc.")
        view = st.segmented_control(
            "View",
            [":material/bar_chart:", ":material/table:"],
            default=":material/bar_chart:",
            required=True,
            key="mastery_view",
            label_visibility="collapsed",
        )

    if view == ":material/table:":
        st.dataframe(
            mastery[["topic", "accuracy", "benchmark", "mastery_score", "attempted", "weightage_marks", "status"]],
            hide_index=True,
            column_config={
                "topic": st.column_config.TextColumn("Topic"),
                "accuracy": st.column_config.ProgressColumn("Accuracy", min_value=0, max_value=100, format="%.1f%%"),
                "benchmark": st.column_config.NumberColumn("Target", format="%d%%"),
                "mastery_score": st.column_config.NumberColumn("Mastery", format="%d / 100"),
                "attempted": st.column_config.NumberColumn("Attempted"),
                "weightage_marks": st.column_config.TextColumn("GATE weightage"),
                "status": st.column_config.TextColumn("Status"),
            },
            alt="Accuracy, target and mastery for each GATE CS topic",
        )
    else:
        topic_order = mastery["topic"].tolist()
        bars = (
            alt.Chart(mastery)
            .mark_bar(cornerRadiusEnd=4, height=18)
            .encode(
                x=alt.X("accuracy:Q", title="Accuracy (%)", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y("topic:N", title=None, sort=topic_order),
                color=alt.Color(
                    "tier:N",
                    title=None,
                    scale=alt.Scale(
                        domain=["Strong", "Moderate", "Weak"],
                        range=[colors["strong"], colors["moderate"], colors["weak"]],
                    ),
                    legend=alt.Legend(orient="bottom"),
                ),
                tooltip=[
                    alt.Tooltip("topic:N", title="Topic"),
                    alt.Tooltip("accuracy:Q", title="Accuracy", format=".1f"),
                    alt.Tooltip("benchmark:Q", title="Target"),
                    alt.Tooltip("weightage_marks:N", title="GATE weightage"),
                ],
            )
        )
        ticks = (
            alt.Chart(mastery)
            .mark_tick(thickness=2.5, size=26, color=colors["benchmark"])
            .encode(x="benchmark:Q", y=alt.Y("topic:N", sort=topic_order))
        )
        st.altair_chart(
            (bars + ticks).properties(height=380),
            alt="Algorithms and data structures lead; compiler design and theory of computation sit well below target",
        )

# --- Weak topics ------------------------------------------------------------
st.subheader("Weak topics", icon=":material/report:")
st.caption("Root causes behind the marks you're losing to negative marking.")

weak_col, audit_col = st.columns([3, 2], gap="medium")

with weak_col:
    for t in WEAKEST_TOPICS:
        with st.container(border=True, gap="xsmall"):
            with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
                st.markdown(f"**{t['topic']}**")
                st.badge(t["badge"], color="red")
            st.markdown(t["primary_issue"])
            st.caption(
                f"Accuracy **{t['accuracy']}%** · Penalty :red[**−{t['negative_marks_lost']}** marks/test] · "
                f"{t['mastery']}"
            )

with audit_col.container(border=True, height="stretch"):
    st.markdown("**Negative marks audit**")
    st.markdown(
        "Removing just **three wrong answers** on 2-mark questions wins back about **8 marks**, "
        "which typically moves your AIR by **150–300 places**."
    )
    st.markdown(
        "- **Theory of computation:** traps in undecidable problems\n"
        "- **Compiler design:** LR(1) lookahead conflicts\n"
        "- **Computer organization:** pipeline hazard stalls"
    )
    if st.button("Practice weak topics", type="primary", icon=":material/target:", width="stretch"):
        ss.practice_topic = "Theory of Computation"
        ss.practice_q_idx = 0
        ss.pop("w_practice_topic", None)
        st.switch_page(PRACTICE_PAGE)

# --- Recommended revision ---------------------------------------------------
st.subheader("Recommended for revision", icon=":material/menu_book:")
st.caption("Ordered by expected score gain per hour of study.")

for plan in RECOMMENDED_REVISIONS:
    icon, color = PRIORITY_STYLE[plan["priority"]]
    with st.container(border=True, gap="xsmall"):
        with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
            st.markdown(f"**{plan['topic']}**")
            label = plan["priority"] if plan["priority"] == "Maintenance" else f"{plan['priority']} priority"
            st.badge(label, icon=icon, color=color)
        st.markdown(plan["action"])
        st.caption(
            f"GATE weightage **{plan['weightage']}** · Current accuracy **{plan['current_accuracy']}** · "
            f"Practice: **{plan['suggested_questions']}**"
        )

with st.expander("Revision checklist", icon=":material/checklist:"):
    left, right = st.columns(2)
    with left:
        st.checkbox("Review decidability vs. Turing-recognisability reduction proofs")
        st.checkbox("Trace LR(0) / SLR(1) shift-reduce conflict examples")
        st.checkbox("Solve 10 TCP Tahoe vs. Reno timeout / 3-dup-ACK numericals", value=True)
    with right:
        st.checkbox("Recalculate 2-way vs. 4-way set-associative cache tag bits", value=True)
        st.checkbox("Revise BCNF decomposition: lossless and dependency-preserving tests", value=True)
        st.checkbox("Practice branch hazard delay slots and operand forwarding paths")
