"""
Mock historical and analytical performance data for GATE CS aspirant.
Provides realistic metrics, test progression history, topic mastery levels, and recommendations.
"""

# 14 completed mock test sessions for GATE CS 2027 preparation (Demo dataset)
TEST_HISTORY = [
    {
        "test_name": "Diagnostic Mock",
        "date": "2026-08-22",
        "questions_count": 60,
        "score": 56.0,
        "max_score": 100,
        "accuracy": 64.0,
        "time_taken_min": 175,
    },
    {
        "test_name": "Sectional: Discrete Math",
        "date": "2026-08-26",
        "questions_count": 50,
        "score": 60.0,
        "max_score": 100,
        "accuracy": 68.5,
        "time_taken_min": 140,
    },
    {
        "test_name": "Full Mock 1",
        "date": "2026-08-30",
        "questions_count": 65,
        "score": 62.5,
        "max_score": 100,
        "accuracy": 71.0,
        "time_taken_min": 172,
    },
    {
        "test_name": "Subject: Digital Logic",
        "date": "2026-09-04",
        "questions_count": 60,
        "score": 64.0,
        "max_score": 100,
        "accuracy": 73.0,
        "time_taken_min": 155,
    },
    {
        "test_name": "Sectional: Core CS",
        "date": "2026-09-08",
        "questions_count": 65,
        "score": 66.0,
        "max_score": 100,
        "accuracy": 74.5,
        "time_taken_min": 168,
    },
    {
        "test_name": "Full Mock 2",
        "date": "2026-09-12",
        "questions_count": 60,
        "score": 67.5,
        "max_score": 100,
        "accuracy": 76.0,
        "time_taken_min": 145,
    },
    {
        "test_name": "Subject: Algo & DS",
        "date": "2026-09-16",
        "questions_count": 65,
        "score": 68.5,
        "max_score": 100,
        "accuracy": 77.0,
        "time_taken_min": 165,
    },
    {
        "test_name": "Sectional: DBMS & OS",
        "date": "2026-09-20",
        "questions_count": 60,
        "score": 70.0,
        "max_score": 100,
        "accuracy": 78.5,
        "time_taken_min": 150,
    },
    {
        "test_name": "Full Mock 3",
        "date": "2026-09-24",
        "questions_count": 65,
        "score": 71.5,
        "max_score": 100,
        "accuracy": 80.0,
        "time_taken_min": 160,
    },
    {
        "test_name": "Subject: Computer Networks",
        "date": "2026-09-28",
        "questions_count": 60,
        "score": 72.0,
        "max_score": 100,
        "accuracy": 80.5,
        "time_taken_min": 148,
    },
    {
        "test_name": "Sectional: Systems",
        "date": "2026-10-02",
        "questions_count": 65,
        "score": 73.0,
        "max_score": 100,
        "accuracy": 81.5,
        "time_taken_min": 162,
    },
    {
        "test_name": "Subject: Theory & Compiler",
        "date": "2026-10-05",
        "questions_count": 60,
        "score": 74.5,
        "max_score": 100,
        "accuracy": 83.0,
        "time_taken_min": 152,
    },
    {
        "test_name": "Subject: Computer Organization",
        "date": "2026-10-08",
        "questions_count": 60,
        "score": 77.0,
        "max_score": 100,
        "accuracy": 84.5,
        "time_taken_min": 146,
    },
    {
        "test_name": "Full Mock 4 (Latest)",
        "date": "2026-10-10",
        "questions_count": 65,
        "score": 76.5,
        "max_score": 100,
        "accuracy": 83.2,
        "time_taken_min": 162,
    },
]

# Backward compatibility aliases
ALL_TESTS = TEST_HISTORY
RECENT_TESTS = TEST_HISTORY[-7:]

# Summary calculated dynamically from the 14 mock sessions to ensure 100% mathematical consistency
_scores = [t["score"] for t in TEST_HISTORY]
_accuracies = [t["accuracy"] for t in TEST_HISTORY]
_questions = [t["questions_count"] for t in TEST_HISTORY]

DASHBOARD_SUMMARY = {
    "avg_score": round(sum(_scores) / len(_scores), 1),  # 959.0 / 14 = 68.5
    "score_delta": "+5.2 pts",
    "score_delta_note": "vs last month",
    "avg_accuracy": round(sum(_accuracies) / len(_accuracies), 1),  # 1075.2 / 14 = 76.8%
    "accuracy_delta": "+3.4%",
    "accuracy_delta_note": "this week",
    "tests_completed": len(TEST_HISTORY),  # exactly 14
    "total_questions_solved": sum(_questions),  # exactly 860
    "current_streak_days": 12,
    "target_exam": "GATE CS 2027",
    "dataset_type": "demo",
}

TOPIC_MASTERY = [
    {
        "topic": "Algorithms",
        "accuracy": 89.5,
        "benchmark": 75,
        "attempted": 140,
        "status": "Strong",
        "weightage_marks": "9-11",
    },
    {
        "topic": "Data Structures",
        "accuracy": 86.0,
        "benchmark": 75,
        "attempted": 120,
        "status": "Strong",
        "weightage_marks": "7-9",
    },
    {
        "topic": "Operating Systems",
        "accuracy": 82.5,
        "benchmark": 70,
        "attempted": 105,
        "status": "Strong",
        "weightage_marks": "8-10",
    },
    {
        "topic": "Database Systems",
        "accuracy": 79.0,
        "benchmark": 70,
        "attempted": 95,
        "status": "Moderate",
        "weightage_marks": "7-8",
    },
    {
        "topic": "Digital Logic",
        "accuracy": 75.0,
        "benchmark": 65,
        "attempted": 75,
        "status": "Moderate",
        "weightage_marks": "5-6",
    },
    {
        "topic": "Computer Networks",
        "accuracy": 64.0,
        "benchmark": 70,
        "attempted": 95,
        "status": "Needs Work",
        "weightage_marks": "8-10",
    },
    {
        "topic": "Theory of Computation",
        "accuracy": 56.5,
        "benchmark": 72,
        "attempted": 90,
        "status": "Weak",
        "weightage_marks": "8-10",
    },
    {
        "topic": "Compiler Design",
        "accuracy": 51.0,
        "benchmark": 70,
        "attempted": 65,
        "status": "Weak",
        "weightage_marks": "4-6",
    },
    {
        "topic": "Computer Organization",
        "accuracy": 60.0,
        "benchmark": 68,
        "attempted": 75,
        "status": "Needs Work",
        "weightage_marks": "7-9",
    },
]

# Highlighted core topics for the dashboard (OS, DBMS, CN, and Algorithms)
CORE_TOPIC_NAMES = ["Algorithms", "Operating Systems", "Database Systems", "Computer Networks"]
CORE_TOPIC_MASTERY = [t for t in TOPIC_MASTERY if t["topic"] in CORE_TOPIC_NAMES]

STRONGEST_TOPICS = [
    {
        "topic": "Algorithms",
        "accuracy": 89.5,
        "badge": "Best performing",
        "highlight": "High speed on Dynamic Programming & Divide-and-Conquer",
    },
    {
        "topic": "Data Structures",
        "accuracy": 86.0,
        "badge": "Consistent",
        "highlight": "Flawless on Trees, Heaps, and Hashing",
    },
    {
        "topic": "Operating Systems",
        "accuracy": 82.5,
        "badge": "Reliable",
        "highlight": "Strong on Process Synchronization & Scheduling",
    },
]

WEAKEST_TOPICS = [
    {
        "topic": "Compiler Design",
        "accuracy": 51.0,
        "badge": "High negative marking",
        "primary_issue": "Parsing tables (LL(1) & LR(0)/SLR(1)) conflict analysis",
        "negative_marks_lost": 4.66,
    },
    {
        "topic": "Theory of Computation",
        "accuracy": 56.5,
        "badge": "Concept trap",
        "primary_issue": "Closure properties and Decidability / Undecidability proofs",
        "negative_marks_lost": 6.33,
    },
    {
        "topic": "Computer Organization",
        "accuracy": 60.0,
        "badge": "Calculation bottleneck",
        "primary_issue": "Pipelining hazards, branch penalties, and Cache latency calculations",
        "negative_marks_lost": 3.66,
    },
]

RECOMMENDED_REVISIONS = [
    {
        "priority": "High",
        "topic": "Theory of Computation - Decidability & Reducibility",
        "weightage": "4-5 marks",
        "current_accuracy": "48%",
        "action": "Review Rice's Theorem and Post Correspondence Problem (PCP)",
        "suggested_questions": "20 PYQs (2015-2024)"
    },
    {
        "priority": "High",
        "topic": "Compiler Design - Bottom-Up Parsing (LR Parsing)",
        "weightage": "3-4 marks",
        "current_accuracy": "50%",
        "action": "Practice constructing LR(1) items and CLR/LALR parser state merging",
        "suggested_questions": "15 Targeted Problems"
    },
    {
        "priority": "Medium",
        "topic": "Computer Networks - TCP Congestion Window & Subnetting",
        "weightage": "4-5 marks",
        "current_accuracy": "61%",
        "action": "Solve numericals on slow start, additive increase, fast retransmit, and CIDR masks",
        "suggested_questions": "18 Numericals"
    },
    {
        "priority": "Medium",
        "topic": "Computer Organization - Pipeline CPI & Structural Hazards",
        "weightage": "3-4 marks",
        "current_accuracy": "58%",
        "action": "Focus on branch penalty, stall calculation, and data forwarding conditions",
        "suggested_questions": "12 Numericals"
    },
    {
        "priority": "Maintenance",
        "topic": "Algorithms - Dynamic Programming & Graph Theory",
        "weightage": "8-10 marks",
        "current_accuracy": "89%",
        "action": "Quick weekly formula brush-up and timed speed tests to maintain accuracy",
        "suggested_questions": "10 Speed Practice Qs"
    }
]
