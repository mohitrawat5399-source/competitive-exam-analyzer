"""
Dashboard view (Landing Page) for Competitive Exam Analyzer.
Displays:
- Average score and accuracy KPI cards
- Recent test performance chart (Plotly)
- Strongest and weakest topics breakdown
- Prominent Start Practice action
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data.mock_history import DASHBOARD_SUMMARY, RECENT_TESTS, STRONGEST_TOPICS, WEAKEST_TOPICS


def render_dashboard():
    # Hero Welcome Banner with Prominent Call to Action
    st.markdown(
        """
        <div class="hero-banner">
            <div class="exam-brand-badge">🎯 GATE CS 2025/2026 Target</div>
            <div class="hero-title">Welcome back, Aspirant! 🚀</div>
            <div class="hero-subtitle">
                Track your progress, pinpoint high-yield weaknesses, and simulate realistic GATE CS test scenarios.
                Your current projected score is <b>{} / 1000</b> (Estimated <b>{}</b>).
            </div>
        </div>
        """.format(
            DASHBOARD_SUMMARY["predicted_gate_score"],
            DASHBOARD_SUMMARY["predicted_rank"]
        ),
        unsafe_allow_html=True
    )

    # Prominent Start Practice CTA Banner
    cta_col1, cta_col2 = st.columns([3, 1])
    with cta_col1:
        st.info("💡 **Ready to boost your percentile?** Try our curated GATE CS Practice Arena with timer and instant diagnostics.")
    with cta_col2:
        if st.button("🚀 Start Practice Now", type="primary", use_container_width=True, key="dashboard_start_practice"):
            st.session_state["nav_selection"] = "Practice"
            st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 1. Average Score, Accuracy, and Performance KPI Cards
    st.markdown("### 📊 Overall Performance Snapshot")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Average Mock Score</div>
                <div class="kpi-value">{DASHBOARD_SUMMARY['avg_score']}<span style="font-size: 1.1rem; color: #94a3b8;"> / 100</span></div>
                <div class="kpi-delta-positive">↗ {DASHBOARD_SUMMARY['score_delta']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Overall Accuracy</div>
                <div class="kpi-value">{DASHBOARD_SUMMARY['avg_accuracy']}%</div>
                <div class="kpi-delta-positive">↗ {DASHBOARD_SUMMARY['accuracy_delta']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Mock Tests Completed</div>
                <div class="kpi-value">{DASHBOARD_SUMMARY['tests_completed']}</div>
                <div class="kpi-delta-neutral">⚡ {DASHBOARD_SUMMARY['total_questions_solved']} Qs Solved</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Predicted Percentile</div>
                <div class="kpi-value">{DASHBOARD_SUMMARY['estimated_percentile']}%</div>
                <div class="kpi-delta-positive">🔥 {DASHBOARD_SUMMARY['current_streak_days']} Day Streak</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # 2. Recent Test Performance Chart
    st.markdown("### 📈 Recent Test Performance Trend")
    st.caption("Track your score progression and accuracy trajectory across recent full-length and sectional tests.")

    df_tests = pd.DataFrame(RECENT_TESTS)

    fig = go.Figure()

    # Score line
    fig.add_trace(go.Scatter(
        x=df_tests["test_name"],
        y=df_tests["score"],
        mode="lines+markers",
        name="Score (out of 100)",
        line=dict(color="#6366f1", width=3.5),
        marker=dict(size=9, color="#818cf8", symbol="circle"),
        hovertemplate="<b>%{x}</b><br>Score: %{y}/100<extra></extra>"
    ))

    # Accuracy line
    fig.add_trace(go.Scatter(
        x=df_tests["test_name"],
        y=df_tests["accuracy"],
        mode="lines+markers",
        name="Accuracy (%)",
        line=dict(color="#10b981", width=2.5, dash="dot"),
        marker=dict(size=8, color="#34d399", symbol="diamond"),
        hovertemplate="<b>%{x}</b><br>Accuracy: %{y}%<extra></extra>"
    ))

    # Target Benchmark line (GATE CS 70 Marks benchmark for top IITs)
    fig.add_trace(go.Scatter(
        x=df_tests["test_name"],
        y=[70] * len(df_tests),
        mode="lines",
        name="IIT Cutoff Benchmark (70)",
        line=dict(color="#f59e0b", width=2, dash="dash"),
        hoverinfo="skip"
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.4)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        height=360,
        margin=dict(l=40, r=30, t=30, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.1)",
            title=""
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.1)",
            title="Score / Accuracy %",
            range=[40, 100]
        ),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 3. Strongest and Weakest Topics Breakdown
    col_strong, col_weak = st.columns(2)

    with col_strong:
        st.markdown("### 🏆 Strongest Topics")
        st.caption("Consistently scoring above the 80% accuracy threshold.")
        for item in STRONGEST_TOPICS:
            st.markdown(
                f"""
                <div class="topic-card-strong">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 1.05rem; font-weight: 700; color: #f8fafc;">{item['topic']}</span>
                        <span class="badge-strong">{item['badge']}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px;">
                        {item['highlight']}
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbd5e1;">
                        <span>Accuracy: <b>{item['accuracy']}%</b></span>
                        <span style="color: #34d399;">Mastery: <b>{item['mastery']}</b></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Streamlit progress bar for visual accuracy fill
            st.progress(item['accuracy'] / 100.0)

    with col_weak:
        st.markdown("### ⚠️ Weakest Topics (Need Attention)")
        st.caption("High negative-marking impact areas requiring targeted revision.")
        for item in WEAKEST_TOPICS:
            st.markdown(
                f"""
                <div class="topic-card-weak">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 1.05rem; font-weight: 700; color: #f8fafc;">{item['topic']}</span>
                        <span class="badge-weak">{item['badge']}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: #fca5a5; margin-bottom: 8px;">
                        ⚠️ {item['primary_issue']}
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbd5e1;">
                        <span>Accuracy: <b>{item['accuracy']}%</b></span>
                        <span style="color: #f87171;">Negative Lost: <b>-{item['negative_marks_lost']} marks</b></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Streamlit progress bar for visual accuracy fill
            st.progress(item['accuracy'] / 100.0)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Recent Test Log Table with Quick Jump
    with st.expander("📋 View Detailed Recent Test Log Table", expanded=False):
        df_display = df_tests[["test_name", "date", "score", "accuracy", "time_taken_min", "rank"]].copy()
        df_display.columns = ["Mock Test Name", "Date", "Score (100)", "Accuracy (%)", "Time (Mins)", "Est. AIR"]
        st.dataframe(df_display, use_container_width=True)
