"""
Custom styling and CSS injections for the Competitive Exam Analyzer Streamlit application.
"""

CUSTOM_CSS = """
<style>
/* Main app container adjustments */
.main .block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 1280px;
}

/* Header & brand styling */
.exam-brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.15), rgba(124, 58, 237, 0.15));
    border: 1px solid rgba(99, 102, 241, 0.35);
    color: #818cf8;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

.hero-banner {
    background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 50%, #172554 100%);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}

.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #94a3b8;
    line-height: 1.5;
    margin-bottom: 18px;
}

/* Custom KPI Metric Cards */
.kpi-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 14px;
    padding: 20px;
    transition: transform 0.2s ease, border-color 0.2s ease;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
}

.kpi-label {
    font-size: 0.85rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
    margin-bottom: 6px;
}

.kpi-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.1;
    margin-bottom: 6px;
}

.kpi-delta-positive {
    font-size: 0.85rem;
    color: #34d399;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.kpi-delta-neutral {
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 600;
}

/* Topic Badge Cards */
.topic-card-strong {
    background: linear-gradient(145deg, rgba(6, 78, 59, 0.25), rgba(15, 23, 42, 0.6));
    border: 1px solid rgba(52, 211, 153, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}

.topic-card-weak {
    background: linear-gradient(145deg, rgba(127, 29, 29, 0.25), rgba(15, 23, 42, 0.6));
    border: 1px solid rgba(248, 113, 113, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}

.badge-strong {
    background: rgba(16, 185, 129, 0.2);
    color: #6ee7b7;
    border: 1px solid rgba(52, 211, 153, 0.4);
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-weak {
    background: rgba(239, 68, 68, 0.2);
    color: #fca5a5;
    border: 1px solid rgba(248, 113, 113, 0.4);
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Practice Exam Arena Box */
.practice-container {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 16px;
    padding: 24px;
    margin-top: 16px;
}

.timer-box {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid rgba(234, 179, 8, 0.4);
    border-radius: 10px;
    padding: 10px 18px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #facc15;
    font-family: monospace;
    font-size: 1.25rem;
    font-weight: 700;
}

.q-meta-tag {
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #c7d2fe;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 6px;
    display: inline-block;
    margin-right: 6px;
}

.question-text-box {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 12px;
    padding: 20px;
    margin: 16px 0;
    font-size: 1.15rem;
    line-height: 1.6;
    color: #f1f5f9;
}

/* Solution Explanation Box */
.solution-box {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(59, 130, 246, 0.4);
    border-left: 5px solid #3b82f6;
    border-radius: 10px;
    padding: 18px;
    margin-top: 18px;
}

/* Call to action button highlight */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    padding: 0.65rem 1.6rem !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 14px 0 rgba(124, 58, 237, 0.39) !important;
    transition: all 0.2s ease !important;
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5) !important;
}

/* Streamlit radio / options padding */
.stRadio > div {
    gap: 10px;
}

/* Hide streamlit default top padding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
