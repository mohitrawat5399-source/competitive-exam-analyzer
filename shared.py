"""
Shared helpers for the Prepmaster app.

Keeps session-state setup, practice grading, and theme-aware chart colours
in one place so the page scripts in ``app_pages/`` stay focused on layout.
"""

import time

import streamlit as st

DASHBOARD_PAGE = "app_pages/dashboard.py"
PRACTICE_PAGE = "app_pages/practice.py"
ANALYSIS_PAGE = "app_pages/analysis.py"

EXAM_DURATION_SECONDS = 3 * 60 * 60  # GATE is a 3-hour paper

STATE_DEFAULTS = {
    "practice_q_idx": 0,
    "user_answers": {},  # question id -> selected option index
    "marked_for_review": set(),  # question ids flagged for review
    "test_submitted": False,
    "latest_test_results": None,
    "practice_exam": "GATE CS",
    "practice_year": "All Years",
    "practice_topic": "All Topics",
    "practice_started_at": None,
}


def init_state() -> None:
    """Initialise every session-state key the app relies on (run once per rerun)."""
    for key, value in STATE_DEFAULTS.items():
        if key not in st.session_state:
            # Copy mutable defaults so sessions never share the same object.
            st.session_state[key] = value.copy() if isinstance(value, (dict, set)) else value


def reset_practice() -> None:
    """Clear answers and restart the current practice session."""
    for key in list(st.session_state.keys()):
        if isinstance(key, str) and key.startswith("answer_"):
            del st.session_state[key]
    st.session_state.user_answers = {}
    st.session_state.marked_for_review = set()
    st.session_state.test_submitted = False
    st.session_state.latest_test_results = None
    st.session_state.practice_q_idx = 0
    st.session_state.practice_started_at = time.time()
    st.toast("Practice session reset", icon=":material/restart_alt:")


def negative_marks(marks: int) -> float:
    """GATE MCQ penalty: one third of the question's marks."""
    return round(marks / 3.0, 2)


def grade(questions: list[dict], answers: dict) -> dict:
    """Score a practice attempt with GATE-style negative marking."""
    total = 0.0
    correct = incorrect = unattempted = 0
    per_question = []

    for q in questions:
        marks = q.get("marks", 2)
        choice = answers.get(q["id"])

        if choice is None:
            unattempted += 1
            earned, status = 0.0, "Unattempted"
        elif choice == q["correct_option_index"]:
            correct += 1
            earned, status = float(marks), "Correct"
        else:
            incorrect += 1
            earned, status = -negative_marks(marks), "Incorrect"

        total += earned
        per_question.append({**q, "user_choice": choice, "earned_marks": earned, "status": status})

    attempted = correct + incorrect
    return {
        "net_score": max(0.0, round(total, 2)),
        "max_marks": sum(q.get("marks", 2) for q in questions),
        "accuracy": round(correct / attempted * 100, 1) if attempted else 0.0,
        "correct_count": correct,
        "incorrect_count": incorrect,
        "unattempted_count": unattempted,
        "results": per_question,
    }


def chart_colors() -> dict:
    """Colours for Altair charts that match the active light/dark theme."""
    if st.context.theme.type == "dark":
        return {
            "primary": "#6CC3A0",
            "accent": "#E0A04A",
            "strong": "#5BB98C",
            "moderate": "#E0A04A",
            "weak": "#E07A5F",
            "muted": "#9A958B",
            "benchmark": "#ECE9E1",
        }
    return {
        "primary": "#1F5F4A",
        "accent": "#C2741A",
        "strong": "#2F7D5B",
        "moderate": "#C2741A",
        "weak": "#B5452F",
        "muted": "#7A756B",
        "benchmark": "#1B1A17",
    }
