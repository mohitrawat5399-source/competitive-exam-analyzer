"""
Practice Arena component for Competitive Exam Analyzer.
Displays:
- Exam selector (GATE CS), Year, and Topic filters
- Interactive countdown / session timer
- Question navigation palette
- Multiple-choice questions with answer choices
- Previous, Next, Mark for Review, and Submit actions
- Instant score computation & solution walkthrough upon submission
"""

import streamlit as st
from data.questions import QUESTIONS_DB, EXAM_OPTIONS, YEAR_OPTIONS, TOPIC_OPTIONS


def init_practice_state():
    """Initializes session state keys for the practice arena if not already set."""
    if "practice_q_idx" not in st.session_state:
        st.session_state["practice_q_idx"] = 0
    if "user_answers" not in st.session_state:
        # Maps question id -> selected_option_index
        st.session_state["user_answers"] = {}
    if "marked_for_review" not in st.session_state:
        # Set of question ids marked for review
        st.session_state["marked_for_review"] = set()
    if "test_submitted" not in st.session_state:
        st.session_state["test_submitted"] = False
    if "practice_exam" not in st.session_state:
        st.session_state["practice_exam"] = "GATE CS"
    if "practice_year" not in st.session_state:
        st.session_state["practice_year"] = "All Years"
    if "practice_topic" not in st.session_state:
        st.session_state["practice_topic"] = "All Topics"


def get_filtered_questions():
    """Filters questions based on user selection in session state."""
    selected_year = st.session_state.get("practice_year", "All Years")
    selected_topic = st.session_state.get("practice_topic", "All Topics")
    selected_exam = st.session_state.get("practice_exam", "GATE CS")

    filtered = []
    for q in QUESTIONS_DB:
        # Exam match
        if q["exam"] != selected_exam and selected_exam == "GATE CS":
            pass # Keep GATE CS
        # Year match
        if selected_year != "All Years" and q["year"] != selected_year:
            continue
        # Topic match
        if selected_topic != "All Topics" and q["topic"] != selected_topic:
            continue
        filtered.append(q)

    # Fallback to all questions if filter leaves empty list
    return filtered if filtered else QUESTIONS_DB


def calculate_test_results(questions):
    """Calculates marks, accuracy, correct count, and incorrect count."""
    total_marks = 0
    max_marks = sum(q.get("marks", 2) for q in questions)
    correct_count = 0
    incorrect_count = 0
    unattempted_count = 0

    question_results = []

    for q in questions:
        qid = q["id"]
        marks = q.get("marks", 2)
        penalty = round(marks / 3.0, 2)
        user_choice = st.session_state["user_answers"].get(qid, None)

        if user_choice is None:
            unattempted_count += 1
            earned = 0.0
            status = "Unattempted"
        elif user_choice == q["correct_option_index"]:
            correct_count += 1
            earned = float(marks)
            total_marks += earned
            status = "Correct"
        else:
            incorrect_count += 1
            earned = -penalty
            total_marks += earned
            status = "Incorrect"

        question_results.append({
            "id": qid,
            "topic": q["topic"],
            "user_choice": user_choice,
            "correct_choice": q["correct_option_index"],
            "earned_marks": earned,
            "status": status,
            "explanation": q["explanation"],
            "question": q["question"],
            "options": q["options"]
        })

    attempted_count = correct_count + incorrect_count
    accuracy = round((correct_count / attempted_count) * 100, 1) if attempted_count > 0 else 0.0
    net_score = max(0.0, round(total_marks, 2))

    return {
        "net_score": net_score,
        "max_marks": max_marks,
        "accuracy": accuracy,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "unattempted_count": unattempted_count,
        "results": question_results
    }


def render_practice():
    init_practice_state()

    st.markdown("## ✍️ GATE CS Practice Arena")
    st.caption("Simulate real exam conditions with timed practice, instant evaluation, and detailed explanations.")

    # Top Filter Controls Row
    filter_col1, filter_col2, filter_col3 = st.columns([1.2, 1, 1.2])

    with filter_col1:
        st.session_state["practice_exam"] = st.selectbox(
            "Target Exam",
            EXAM_OPTIONS,
            index=0,
            key="select_practice_exam"
        )

    with filter_col2:
        st.session_state["practice_year"] = st.selectbox(
            "Filter by Year (PYQ)",
            YEAR_OPTIONS,
            index=YEAR_OPTIONS.index(st.session_state["practice_year"]) if st.session_state["practice_year"] in YEAR_OPTIONS else 0,
            key="select_practice_year"
        )

    with filter_col3:
        st.session_state["practice_topic"] = st.selectbox(
            "Filter by Topic / Subject",
            TOPIC_OPTIONS,
            index=TOPIC_OPTIONS.index(st.session_state["practice_topic"]) if st.session_state["practice_topic"] in TOPIC_OPTIONS else 0,
            key="select_practice_topic"
        )

    questions = get_filtered_questions()
    total_q = len(questions)

    # Make sure current question index is within range
    if st.session_state["practice_q_idx"] >= total_q:
        st.session_state["practice_q_idx"] = 0

    curr_idx = st.session_state["practice_q_idx"]
    curr_q = questions[curr_idx]
    qid = curr_q["id"]

    st.markdown("<hr style='margin: 12px 0 18px 0; border-color: rgba(148, 163, 184, 0.15);'>", unsafe_allow_html=True)

    # Top Timer & Status Bar
    header_col1, header_col2, header_col3 = st.columns([2, 2, 2])

    with header_col1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="q-meta-tag">Question {curr_idx + 1} of {total_q}</span>
                <span class="q-meta-tag" style="background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3); color: #6ee7b7;">
                    +{curr_q['marks']} Marks | -{round(curr_q['marks']/3.0, 2)} Neg
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with header_col2:
        st.markdown(
            f"""
            <span class="q-meta-tag" style="background: rgba(245, 158, 11, 0.15); border-color: rgba(245, 158, 11, 0.3); color: #fcd34d;">
                🏷️ {curr_q['topic']} ({curr_q['year']})
            </span>
            <span class="q-meta-tag" style="background: rgba(148, 163, 184, 0.15); border-color: rgba(148, 163, 184, 0.3); color: #cbd5e1;">
                Level: {curr_q['difficulty']}
            </span>
            """,
            unsafe_allow_html=True
        )

    with header_col3:
        # Display simulated live exam countdown timer
        st.markdown(
            """
            <div style="text-align: right;">
                <span class="timer-box">⏱️ 02:45 / 03:00 Remaining</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Question Navigation Palette & Main Question Layout
    main_q_col, nav_palette_col = st.columns([3.5, 1.2])

    with main_q_col:
        # Question Statement Card
        st.markdown(
            f"""
            <div class="question-text-box">
                <div style="font-weight: 600; font-size: 0.95rem; color: #818cf8; margin-bottom: 6px;">
                    Question ID: {curr_q['id']} &bull; {curr_q['subtopic']}
                </div>
                <div style="font-size: 1.15rem; color: #f8fafc; font-weight: 500;">
                    {curr_q['question']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Answer choices (Multiple Choice)
        st.markdown("#### Select Answer Choice:")

        current_saved_answer = st.session_state["user_answers"].get(qid, None)
        options_labels = [f"**({chr(65+i)})** {opt}" for i, opt in enumerate(curr_q["options"])]

        # Find initial index for radio button
        initial_radio_index = current_saved_answer if current_saved_answer is not None else None

        selected_radio = st.radio(
            label="Options",
            options=range(len(options_labels)),
            format_func=lambda i: options_labels[i],
            index=initial_radio_index,
            key=f"radio_{qid}_{curr_idx}",
            label_visibility="collapsed"
        )

        # Update session state answer if selected
        if selected_radio is not None:
            st.session_state["user_answers"][qid] = selected_radio

        # Bottom Question Actions: Previous, Mark for Review, Clear, Next, Submit
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        act_col1, act_col2, act_col3, act_col4 = st.columns([1, 1.4, 1.2, 1])

        with act_col1:
            if st.button("⬅ Previous", disabled=(curr_idx == 0), use_container_width=True, key="btn_prev"):
                st.session_state["practice_q_idx"] = max(0, curr_idx - 1)
                st.rerun()

        with act_col2:
            is_marked = qid in st.session_state["marked_for_review"]
            mark_btn_label = "Unmark Review" if is_marked else "🔖 Mark for Review"
            if st.button(mark_btn_label, use_container_width=True, key="btn_mark_review"):
                if is_marked:
                    st.session_state["marked_for_review"].remove(qid)
                else:
                    st.session_state["marked_for_review"].add(qid)
                st.rerun()

        with act_col3:
            if st.button("🔄 Clear Choice", use_container_width=True, key="btn_clear_choice"):
                if qid in st.session_state["user_answers"]:
                    del st.session_state["user_answers"][qid]
                st.rerun()

        with act_col4:
            if st.button("Next ➡", disabled=(curr_idx == total_q - 1), type="secondary", use_container_width=True, key="btn_next"):
                st.session_state["practice_q_idx"] = min(total_q - 1, curr_idx + 1)
                st.rerun()

    # Question Navigation Palette
    with nav_palette_col:
        st.markdown("#### 🧭 Question Palette")
        st.caption("Jump directly to any question:")

        # Palette grid
        cols_per_row = 4
        for row_start in range(0, total_q, cols_per_row):
            p_cols = st.columns(cols_per_row)
            for offset in range(cols_per_row):
                q_num = row_start + offset
                if q_num < total_q:
                    target_q = questions[q_num]
                    t_qid = target_q["id"]
                    is_answered = t_qid in st.session_state["user_answers"]
                    is_flagged = t_qid in st.session_state["marked_for_review"]
                    is_current = (q_num == curr_idx)

                    # Icon / badge indication
                    btn_text = f"Q{q_num + 1}"
                    if is_current:
                        btn_text = f"▶{q_num + 1}"
                    elif is_flagged:
                        btn_text = f"🏷️{q_num + 1}"
                    elif is_answered:
                        btn_text = f"✓{q_num + 1}"

                    with p_cols[offset]:
                        if st.button(
                            btn_text,
                            key=f"palette_btn_{q_num}",
                            use_container_width=True,
                            type="primary" if is_current else "secondary"
                        ):
                            st.session_state["practice_q_idx"] = q_num
                            st.rerun()

        st.markdown(
            """
            <div style="margin-top: 14px; font-size: 0.8rem; color: #94a3b8; border-top: 1px solid rgba(148, 163, 184, 0.2); padding-top: 8px;">
                <div>🟢 <b>✓</b> Answered ({})</div>
                <div>🏷️ <b>🏷️</b> Marked for Review ({})</div>
                <div>⚪ <b>Q#</b> Unanswered ({})</div>
            </div>
            """.format(
                len(st.session_state["user_answers"]),
                len(st.session_state["marked_for_review"]),
                total_q - len(st.session_state["user_answers"])
            ),
            unsafe_allow_html=True
        )

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Submit Practice Test Button
        if st.button("🚀 Submit Practice Test", type="primary", use_container_width=True, key="btn_submit_test"):
            st.session_state["test_submitted"] = True
            st.rerun()

    # Results & Detailed Solutions Section if Test is Submitted
    if st.session_state.get("test_submitted", False):
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 🎯 Practice Session Results & Instant Diagnostic")

        results_data = calculate_test_results(questions)

        # Store latest practice session in session_state for the Analysis tab to view!
        st.session_state["latest_test_results"] = results_data

        res1, res2, res3, res4 = st.columns(4)
        with res1:
            st.metric("Score Achieved", f"{results_data['net_score']} / {results_data['max_marks']}")
        with res2:
            st.metric("Accuracy Rate", f"{results_data['accuracy']}%")
        with res3:
            st.metric("Correct Answers", f"{results_data['correct_count']} / {total_q}")
        with res4:
            st.metric("Incorrect / Skipped", f"{results_data['incorrect_count']} / {results_data['unattempted_count']}")

        st.info("💡 **Great effort!** You can inspect each question's detailed step-by-step solution below, or jump directly into the full diagnostic dashboard.")

        cta_col1, cta_col2 = st.columns([2, 1])
        with cta_col2:
            if st.button("📈 Open Comprehensive Analysis Tab", type="primary", use_container_width=True, key="btn_jump_to_analysis"):
                st.session_state["nav_selection"] = "Analysis"
                st.rerun()

        # Detailed Question Walkthrough
        with st.expander("🔍 Review Detailed Solutions & Explanations", expanded=True):
            for i, r in enumerate(results_data["results"]):
                status_color = "#34d399" if r["status"] == "Correct" else ("#f87171" if r["status"] == "Incorrect" else "#94a3b8")
                st.markdown(
                    f"""
                    <div class="solution-box">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">Q{i+1}: {r['id']} ({r['topic']})</span>
                            <span style="color: {status_color}; font-weight: 700;">Status: {r['status']} ({r['earned_marks']:+} marks)</span>
                        </div>
                        <div style="color: #cbd5e1; margin-bottom: 10px;">{r['question']}</div>
                        <div style="font-size: 0.95rem; margin-bottom: 8px;">
                            <b>Your Answer:</b> {r['options'][r['user_choice']] if r['user_choice'] is not None else '<span style="color: #94a3b8;">Not Attempted</span>'} <br>
                            <b>Correct Answer:</b> <span style="color: #34d399;">{r['options'][r['correct_choice']]}</span>
                        </div>
                        <div style="background: rgba(30, 41, 59, 0.7); border-radius: 8px; padding: 12px; margin-top: 8px;">
                            <b style="color: #60a5fa;">💡 Detailed Solution:</b><br>
                            <span style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.5;">{r['explanation']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
