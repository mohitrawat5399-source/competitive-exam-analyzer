"""
Analysis and diagnostics.

- Sample score and accuracy (uses the latest practice attempt when available)
- Topic mastery chart vs. target benchmark
- Weak-topic list with negative-marking diagnosis
- Recommended topics for revision
"""

from datetime import date

import altair as alt
import pandas as pd
import streamlit as st

from data.mock_history import RECOMMENDED_REVISIONS, TOPIC_MASTERY, WEAKEST_TOPICS
from shared import PRACTICE_PAGE, chart_colors, init_state

init_state()
ss = st.session_state
colors = chart_colors()
PRIORITY_STYLE = {
    "High": (":material/priority_high:", "red"),
    "Medium": (":material/schedule:", "orange"),
    "Maintenance": (":material/check:", "green"),
}

# --- Header -----------------------------------------------------------------
with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
    st.caption("GATE CS 2027 · Performance Diagnostics")
    st.badge("Demo dataset", icon=":material/science:", color="secondary")

st.title("Performance diagnostics")
st.markdown("Detailed breakdown of your accuracy trends, topic proficiencies, and an actionable revision roadmap.")

latest = ss.get("latest_test_results")
if latest:
    score, max_score = latest["net_score"], latest["max_marks"]
    accuracy = latest["accuracy"]
    correct, incorrect, skipped = latest["correct_count"], latest["incorrect_count"], latest["unattempted_count"]
    source = f"Live Practice Attempt ({date.today():%d %b %Y})"
else:
    score, max_score, accuracy = 76.5, 100, 83.2
    correct, incorrect, skipped = 48, 11, 6
    source = "Full Mock 4 (10 Oct 2026)"

with st.container(horizontal=True, gap="small", vertical_alignment="center"):
    st.caption("Diagnostic source")
    st.badge(source, icon=":material/dataset:", color="primary")

if not latest:
    st.info("Displaying diagnostic results from **Full Mock 4 (10 Oct 2026)** (Demo dataset for GATE CS 2027). Complete a live session in the Practice tab to evaluate your newest test in real time.", icon=":material/info:")

# --- Score and accuracy -----------------------------------------------------
total_q = correct + incorrect + skipped
attempt_rate = round((correct + incorrect) / total_q * 100, 1) if total_q else 0.0

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
        "Attempt rate",
        f"{attempt_rate}%",
        f"{correct + incorrect} of {total_q} questions",
        delta_arrow="off",
        delta_color="off",
        border=True,
    )

# --- Topic mastery ----------------------------------------------------------
mastery = pd.DataFrame(TOPIC_MASTERY).sort_values("accuracy", ascending=False)
mastery["tier"] = pd.cut(
    mastery["accuracy"], bins=[0, 65, 80, 101], labels=["Weak", "Moderate", "Strong"], right=False
).astype(str)

st.subheader("Topic performance & diagnostics", icon=":material/bar_chart:")
st.caption("Detailed evaluation of subject proficiencies against the 70% benchmark across all GATE CS core areas.")

with st.container(border=True):
    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        with st.container(gap="xsmall"):
            st.markdown("**Topic accuracy vs. target benchmark**")
            st.caption("Bars show your accuracy; the tick marks the 70% target benchmark.")
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
            mastery[["topic", "accuracy", "benchmark", "attempted", "weightage_marks", "status"]],
            hide_index=True,
            column_config={
                "topic": st.column_config.TextColumn("Topic"),
                "accuracy": st.column_config.ProgressColumn("Accuracy", min_value=0, max_value=100, format="%.1f%%"),
                "benchmark": st.column_config.NumberColumn("Target", format="%d%%"),
                "attempted": st.column_config.NumberColumn("Attempted"),
                "weightage_marks": st.column_config.TextColumn("GATE weightage"),
                "status": st.column_config.TextColumn("Status"),
            },
            alt="Accuracy, target and status for each GATE CS topic",
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
st.subheader("Weak topics & negative marking audit", icon=":material/report:")
st.caption("Root-cause breakdown of syllabus areas where negative marking is eroding your score.")

weak_col, audit_col = st.columns([3, 2], gap="medium")

with weak_col:
    for t in WEAKEST_TOPICS:
        with st.container(border=True, gap="xsmall"):
            with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
                st.markdown(f"**{t['topic']}**")
                st.badge(t["badge"], color="red")
            st.markdown(t["primary_issue"])
            st.caption(
                f"Accuracy **{t['accuracy']}%** · Penalty :red[**−{t['negative_marks_lost']}** marks/test]"
            )

with audit_col.container(border=True, height="stretch"):
    st.markdown("**Negative marks audit**")
    st.markdown(
        "Removing just **three wrong answers** on 2-mark questions recovers **8 marks** in net score, "
        "preventing significant score erosion from negative deductions."
    )
    st.markdown(
        "- **Theory of computation:** traps in undecidable problems\n"
        "- **Compiler design:** LR(1) lookahead conflicts\n"
        "- **Computer organization:** pipeline hazard stalls"
    )
    if st.button("Start PYQ Practice on weak topics", type="primary", icon=":material/target:", width="stretch"):
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
