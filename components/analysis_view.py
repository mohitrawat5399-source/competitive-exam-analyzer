"""
Analysis & Diagnostic component for Competitive Exam Analyzer.
Displays:
- Sample score and accuracy metrics (with sync to latest test attempt if available)
- Topic mastery chart (Plotly comparison vs benchmark)
- Weak-topic list with error analysis & negative marking diagnosis
- Recommended topics for revision with actionable study roadmap
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data.mock_history import (
    DASHBOARD_SUMMARY,
    TOPIC_MASTERY,
    WEAKEST_TOPICS,
    RECOMMENDED_REVISIONS
)


def render_analysis():
    st.markdown("## 📈 Performance Analysis & Deep Diagnostics")
    st.caption("Identify high-yield improvement areas, review topic mastery, and follow a personalized revision roadmap.")

    # 1. Sample Score and Accuracy Cards
    latest_attempt = st.session_state.get("latest_test_results", None)

    if latest_attempt:
        sample_score = latest_attempt["net_score"]
        sample_max = latest_attempt["max_marks"]
        sample_acc = latest_attempt["accuracy"]
        sample_correct = latest_attempt["correct_count"]
        sample_incorrect = latest_attempt["incorrect_count"]
        sample_unattempted = latest_attempt["unattempted_count"]
        source_label = "Latest Interactive Practice Session"
    else:
        sample_score = 76.5
        sample_max = 100
        sample_acc = 83.2
        sample_correct = 48
        sample_incorrect = 11
        sample_unattempted = 6
        source_label = "GATE Full-Length Mock 4 (Benchmarked)"

    st.markdown(
        f"""
        <div style="background: rgba(30, 41, 59, 0.4); border-left: 4px solid #6366f1; padding: 12px 18px; border-radius: 8px; margin-bottom: 20px;">
            <span style="color: #94a3b8; font-size: 0.88rem;">DIAGNOSTIC DATASET:</span>
            <span style="color: #f8fafc; font-weight: 600; margin-left: 6px;">{source_label}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Sample Score</div>
                <div class="kpi-value">{sample_score}<span style="font-size: 1.1rem; color: #94a3b8;"> / {sample_max}</span></div>
                <div class="kpi-delta-positive">🏆 {round((sample_score/sample_max)*100, 1)}% Score Ratio</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Sample Accuracy</div>
                <div class="kpi-value">{sample_acc}%</div>
                <div class="kpi-delta-positive">🎯 Benchmark: ≥ 75%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Question Breakdown</div>
                <div class="kpi-value" style="font-size: 1.6rem; color: #34d399;">{sample_correct} <span style="font-size: 0.9rem; color: #94a3b8;">Corr</span> | <span style="color: #f87171;">{sample_incorrect}</span> <span style="font-size: 0.9rem; color: #94a3b8;">Inc</span></div>
                <div class="kpi-delta-neutral">⚪ {sample_unattempted} Unattempted</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Projected AIR</div>
                <div class="kpi-value" style="font-size: 1.6rem;">{DASHBOARD_SUMMARY['predicted_rank']}</div>
                <div class="kpi-delta-positive">Top {100 - DASHBOARD_SUMMARY['estimated_percentile']:.1f}% Percentile</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # 2. Topic Mastery Chart
    st.markdown("### 📊 Topic Mastery vs GATE Cutoff Benchmark")
    st.caption("Comparison of your individual accuracy against the target benchmark (70-75%) required for top tier IITs / IISc.")

    df_mastery = pd.DataFrame(TOPIC_MASTERY)
    df_mastery = df_mastery.sort_values(by="accuracy", ascending=True)

    # Color mapping based on performance
    bar_colors = []
    for acc in df_mastery["accuracy"]:
        if acc >= 80:
            bar_colors.append("#10b981")  # Emerald
        elif acc >= 65:
            bar_colors.append("#f59e0b")  # Amber
        else:
            bar_colors.append("#ef4444")  # Rose

    fig = go.Figure()

    # User accuracy bar
    fig.add_trace(go.Bar(
        y=df_mastery["topic"],
        x=df_mastery["accuracy"],
        orientation="h",
        name="Your Accuracy (%)",
        marker=dict(color=bar_colors, opacity=0.9),
        text=[f"{acc}%" for acc in df_mastery["accuracy"]],
        textposition="inside",
        insidetextanchor="end",
        hovertemplate="<b>%{y}</b><br>Accuracy: %{x}%<extra></extra>"
    ))

    # Benchmark target marker
    fig.add_trace(go.Scatter(
        y=df_mastery["topic"],
        x=df_mastery["benchmark"],
        mode="markers",
        name="Target Benchmark",
        marker=dict(size=12, color="#38bdf8", symbol="diamond", line=dict(color="#ffffff", width=1.5)),
        hovertemplate="<b>%{y}</b><br>Target Cutoff: %{x}%<extra></extra>"
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.4)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        height=400,
        margin=dict(l=40, r=40, t=30, b=40),
        xaxis=dict(
            title="Accuracy (%)",
            range=[0, 100],
            gridcolor="rgba(148, 163, 184, 0.1)"
        ),
        yaxis=dict(
            title="",
            gridcolor="rgba(148, 163, 184, 0.1)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 3. Weak-Topic List
    st.markdown("### ⚠️ Detailed Weak-Topic Diagnostic List")
    st.caption("Root-cause breakdown of topics where negative marks are costing rank positions.")

    weak_col1, weak_col2 = st.columns([2, 1.2])

    with weak_col1:
        for idx, item in enumerate(WEAKEST_TOPICS):
            st.markdown(
                f"""
                <div class="topic-card-weak" style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 1.1rem; font-weight: 700; color: #ffffff;">{item['topic']}</span>
                        <span class="badge-weak">{item['badge']}</span>
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.92rem; margin: 8px 0;">
                        <b>Diagnostic Finding:</b> {item['primary_issue']}
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid rgba(248, 113, 113, 0.2); padding-top: 8px;">
                        <span>Current Accuracy: <b style="color: #f87171;">{item['accuracy']}%</b></span>
                        <span>Estimated Penalty: <b style="color: #fca5a5;">-{item['negative_marks_lost']} marks/test</b></span>
                        <span>Status: <b style="color: #f87171;">{item['mastery']}</b></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with weak_col2:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 18px;">
                <h4 style="margin-top: 0; color: #f8fafc;">💡 Negative Marks Audit</h4>
                <p style="font-size: 0.9rem; color: #94a3b8;">
                    In GATE CS, eliminating <b>3 negative answers</b> in 2-mark questions recovers <b>8 marks</b>,
                    which typically improves All India Rank by <b>150 to 300 ranks</b>!
                </p>
                <div style="background: rgba(15, 23, 42, 0.6); padding: 12px; border-radius: 8px; font-size: 0.85rem; color: #cbd5e1;">
                    <div>❌ <b>Theory of Computation:</b> Trap in undecidable problems.</div>
                    <div style="margin-top: 6px;">❌ <b>Compiler Design:</b> LR(1) lookahead conflicts.</div>
                    <div style="margin-top: 6px;">❌ <b>Computer Organization:</b> Pipelining hazard stalls.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        if st.button("🎯 Practice Weak Topics Now", type="primary", use_container_width=True, key="btn_practice_weak"):
            st.session_state["practice_topic"] = "Theory of Computation"
            st.session_state["nav_selection"] = "Practice"
            st.rerun()

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # 4. Recommended Topics for Revision
    st.markdown("### 📋 Recommended Topics for Revision & Action Plan")
    st.caption("AI-prioritized syllabus areas designed to maximize score gain per study hour.")

    for plan in RECOMMENDED_REVISIONS:
        priority_color = "#f87171" if "High" in plan["priority"] else ("#facc15" if "Medium" in plan["priority"] else "#34d399")
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(148, 163, 184, 0.15); border-left: 4px solid {priority_color}; border-radius: 10px; padding: 16px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; font-size: 1.05rem; color: #f8fafc;">{plan['topic']}</span>
                    <span style="color: {priority_color}; font-weight: 600; font-size: 0.85rem;">{plan['priority']}</span>
                </div>
                <div style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 8px;">
                    <b>Recommended Action:</b> {plan['action']}
                </div>
                <div style="display: flex; gap: 20px; font-size: 0.85rem; color: #94a3b8;">
                    <span>GATE Weightage: <b style="color: #f8fafc;">{plan['weightage']}</b></span>
                    <span>Current Accuracy: <b style="color: #f8fafc;">{plan['current_accuracy']}</b></span>
                    <span>Target Practice: <b style="color: #818cf8;">{plan['suggested_questions']}</b></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    with st.expander("📝 Personalized Revision Checklist", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.checkbox("Review Decidability vs Turing Recognizability reduction proofs", value=False)
            st.checkbox("Trace LR(0) / SLR(1) parsing table shift-reduce conflict examples", value=False)
            st.checkbox("Solve 10 TCP Tahoe vs Reno timeout vs 3-dup ACK numericals", value=True)
        with c2:
            st.checkbox("Recalculate 2-way vs 4-way set associative cache tag directory bits", value=True)
            st.checkbox("Revise BCNF decomposition lossless and dependency preserving tests", value=True)
            st.checkbox("Practice branch hazard delay slots and operand forwarding paths", value=False)
