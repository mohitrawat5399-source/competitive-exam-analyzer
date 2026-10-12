"""
Practice arena.

- Select GATE CS and a year or topic
- Sample multiple-choice question (LaTeX renders natively)
- Timer, question navigation palette, and answer choices
- Previous / Next / Mark for review / Clear, and Submit with instant grading
"""

import time

import streamlit as st

from data.questions import EXAM_OPTIONS, QUESTIONS_DB, TOPIC_OPTIONS, YEAR_OPTIONS
from shared import ANALYSIS_PAGE, EXAM_DURATION_SECONDS, grade, negative_marks

ss = st.session_state
if ss.practice_started_at is None:
    ss.practice_started_at = time.time()

DIFFICULTY_COLORS = {"Easy": "green", "Medium": "orange", "Hard": "red"}
STATUS_STYLE = {
    "Correct": (":material/check_circle:", "green"),
    "Incorrect": (":material/cancel:", "red"),
    "Unattempted": (":material/radio_button_unchecked:", "gray"),
}


# --- Callbacks (run before the next script pass, so no st.rerun needed) ------
def sync_filter(state_key: str, widget_key: str) -> None:
    value = ss.get(widget_key)
    if value is not None:
        ss[state_key] = value
    ss.practice_q_idx = 0


def go_to(index: int) -> None:
    ss.practice_q_idx = index


def save_answer(qid: str) -> None:
    choice = ss.get(f"answer_{qid}")
    if choice is None:
        ss.user_answers.pop(qid, None)
    else:
        ss.user_answers[qid] = choice


def clear_answer(qid: str) -> None:
    ss.user_answers.pop(qid, None)
    ss.pop(f"answer_{qid}", None)


def toggle_review(qid: str) -> None:
    ss.marked_for_review ^= {qid}


def submit() -> None:
    ss.test_submitted = True


# --- Header -----------------------------------------------------------------
st.caption("Practice arena")
st.title("Timed practice")
st.markdown("Real GATE CS questions with exam-style marking. Your answers carry over to the analysis tab.")

# --- Filters ----------------------------------------------------------------
exam_col, year_col, topic_col = st.columns([1, 1.5, 1.2], vertical_alignment="bottom")
exam_col.selectbox(
    "Exam",
    EXAM_OPTIONS,
    index=EXAM_OPTIONS.index(ss.practice_exam),
    key="w_practice_exam",
    on_change=sync_filter,
    args=("practice_exam", "w_practice_exam"),
)
with year_col:
    st.segmented_control(
        "Year",
        YEAR_OPTIONS,
        default=ss.practice_year,
        format_func=lambda y: "All years" if y == "All Years" else y,
        required=True,
        key="w_practice_year",
        on_change=sync_filter,
        args=("practice_year", "w_practice_year"),
    )
topic_col.selectbox(
    "Topic",
    TOPIC_OPTIONS,
    index=TOPIC_OPTIONS.index(ss.practice_topic),
    format_func=lambda t: "All topics" if t == "All Topics" else t,
    key="w_practice_topic",
    on_change=sync_filter,
    args=("practice_topic", "w_practice_topic"),
)

questions = [
    q
    for q in QUESTIONS_DB
    if (ss.practice_year == "All Years" or q["year"] == ss.practice_year)
    and (ss.practice_topic == "All Topics" or q["topic"] == ss.practice_topic)
]
if not questions:
    st.caption(":orange[:material/info: No questions match that combination yet, so showing the full set.]")
    questions = QUESTIONS_DB

total = len(questions)
if ss.practice_q_idx >= total:
    ss.practice_q_idx = 0
idx = ss.practice_q_idx
q = questions[idx]
qid = q["id"]
submitted = ss.test_submitted


@st.fragment(run_every="1s")
def exam_timer() -> None:
    if ss.test_submitted:
        st.badge("Submitted", icon=":material/check:", color="green")
        return
    remaining = max(0, int(EXAM_DURATION_SECONDS - (time.time() - ss.practice_started_at)))
    hours, rest = divmod(remaining, 3600)
    minutes, seconds = divmod(rest, 60)
    st.markdown(f":material/timer: **{hours:02d}:{minutes:02d}:{seconds:02d}** :gray[left]")


question_col, palette_col = st.columns([3, 1], gap="medium")

# --- Question card ----------------------------------------------------------
with question_col.container(border=True):
    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        st.markdown(f"**Question {idx + 1}** :gray[of {total}]")
        exam_timer()

    with st.container(horizontal=True, gap="small"):
        st.badge(q["topic"], color="primary")
        st.badge(q["year"], icon=":material/calendar_today:", color="gray")
        st.badge(q["difficulty"], color=DIFFICULTY_COLORS.get(q["difficulty"], "gray"))
        st.badge(f"+{q['marks']} / −{negative_marks(q['marks'])}", icon=":material/balance:", color="gray")
        if qid in ss.marked_for_review:
            st.badge("Marked for review", icon=":material/bookmark:", color="violet")

    st.caption(f"{qid} · {q['subtopic']}")
    st.markdown(q["question"])

    st.radio(
        "Your answer",
        options=range(len(q["options"])),
        format_func=lambda i: f"**{chr(65 + i)}.** {q['options'][i]}",
        index=ss.user_answers.get(qid),
        key=f"answer_{qid}",
        on_change=save_answer,
        args=(qid,),
        disabled=submitted,
    )

    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        with st.container(horizontal=True, gap="small", width="content"):
            st.button(
                "Previous",
                icon=":material/arrow_back:",
                disabled=idx == 0,
                on_click=go_to,
                args=(idx - 1,),
            )
            flagged = qid in ss.marked_for_review
            st.button(
                "Unmark" if flagged else "Mark for review",
                icon=":material/bookmark_remove:" if flagged else ":material/bookmark_add:",
                type="tertiary",
                on_click=toggle_review,
                args=(qid,),
                disabled=submitted,
            )
            st.button(
                "Clear",
                icon=":material/backspace:",
                type="tertiary",
                on_click=clear_answer,
                args=(qid,),
                disabled=submitted or qid not in ss.user_answers,
            )
        st.button(
            "Next",
            icon=":material/arrow_forward:",
            icon_position="right",
            disabled=idx == total - 1,
            on_click=go_to,
            args=(idx + 1,),
        )

# --- Question palette -------------------------------------------------------
with palette_col.container(border=True):
    st.markdown("**Question palette**")
    per_row = 4
    for row_start in range(0, total, per_row):
        cols = st.columns(per_row, gap="xsmall")
        for offset, col in enumerate(cols):
            n = row_start + offset
            if n >= total:
                continue
            target = questions[n]["id"]
            icon = None
            if target in ss.marked_for_review:
                icon = ":material/bookmark:"
            elif target in ss.user_answers:
                icon = ":material/check:"
            col.button(
                str(n + 1),
                key=f"palette_{n}",
                icon=icon,
                type="primary" if n == idx else "secondary",
                width="stretch",
                on_click=go_to,
                args=(n,),
            )

    answered = sum(1 for x in questions if x["id"] in ss.user_answers)
    flagged_count = sum(1 for x in questions if x["id"] in ss.marked_for_review)
    st.caption(
        f":material/check: {answered} answered  \n"
        f":material/bookmark: {flagged_count} marked for review  \n"
        f":material/radio_button_unchecked: {total - answered} unanswered"
    )

    st.button(
        "Submit test",
        type="primary",
        icon=":material/task_alt:",
        width="stretch",
        on_click=submit,
        disabled=submitted,
    )

# --- Results ----------------------------------------------------------------
if submitted:
    results = grade(questions, ss.user_answers)
    ss.latest_test_results = results

    st.space("medium")
    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        st.subheader("Your results", icon=":material/assignment_turned_in:")
        if st.button("Open full analysis", icon=":material/insights:", type="primary"):
            st.switch_page(ANALYSIS_PAGE)

    with st.container(horizontal=True):
        st.metric("Score", f"{results['net_score']} / {results['max_marks']}", border=True)
        st.metric("Accuracy", f"{results['accuracy']}%", border=True)
        st.metric("Correct", f"{results['correct_count']} / {total}", border=True)
        st.metric(
            "Incorrect · skipped",
            f"{results['incorrect_count']} · {results['unattempted_count']}",
            border=True,
        )

    st.markdown("**Solutions**")
    for i, r in enumerate(results["results"]):
        icon, color = STATUS_STYLE[r["status"]]
        with st.expander(f"Question {i + 1} · {r['topic']}", icon=icon):
            with st.container(horizontal=True, gap="small"):
                st.badge(r["status"], color=color)
                st.badge(f"{r['earned_marks']:+g} marks", color="gray")
            st.markdown(r["question"])
            yours = (
                f"{chr(65 + r['user_choice'])}. {r['options'][r['user_choice']]}"
                if r["user_choice"] is not None
                else ":gray[Not attempted]"
            )
            correct = r["correct_option_index"]
            st.markdown(
                f"**Your answer:** {yours}  \n"
                f"**Correct answer:** :green[{chr(65 + correct)}. {r['options'][correct]}]"
            )
            with st.container(border=True):
                st.markdown("**Solution**")
                st.markdown(r["explanation"].replace("\n", "  \n"))
