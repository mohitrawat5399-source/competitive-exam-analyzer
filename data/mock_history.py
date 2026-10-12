"""
Mock historical and analytical performance data for GATE CS aspirant.
Provides realistic metrics, test progression history, topic mastery levels, and recommendations.
"""

DASHBOARD_SUMMARY = {
    "avg_score": 68.5,
    "score_delta": "+5.2 pts",
    "score_delta_note": "vs last month",
    "avg_accuracy": 77.8,
    "accuracy_delta": "+3.4%",
    "accuracy_delta_note": "this week",
    "tests_completed": 14,
    "total_questions_solved": 860,
    "current_streak_days": 12,
    "predicted_gate_score": 745,
    "predicted_rank": "AIR 240–320",
    "estimated_percentile": 98.4
}

RECENT_TESTS = [
    {
        "test_name": "Full Mock 1",
        "date": "2026-09-05",
        "score": 54.0,
        "max_score": 100,
        "accuracy": 62.5,
        "time_taken_min": 172,
        "rank": 820
    },
    {
        "test_name": "Sectional: Core CS",
        "date": "2026-09-12",
        "score": 58.5,
        "max_score": 100,
        "accuracy": 67.0,
        "time_taken_min": 160,
        "rank": 640
    },
    {
        "test_name": "Full Mock 2",
        "date": "2026-09-19",
        "score": 62.0,
        "max_score": 100,
        "accuracy": 71.5,
        "time_taken_min": 165,
        "rank": 510
    },
    {
        "test_name": "Subject: Algo & DS",
        "date": "2026-09-26",
        "score": 74.0,
        "max_score": 100,
        "accuracy": 82.0,
        "time_taken_min": 145,
        "rank": 320
    },
    {
        "test_name": "Full Mock 3",
        "date": "2026-10-02",
        "score": 69.5,
        "max_score": 100,
        "accuracy": 76.5,
        "time_taken_min": 158,
        "rank": 390
    },
    {
        "test_name": "Sectional: Systems (OS/CN)",
        "date": "2026-10-06",
        "score": 71.0,
        "max_score": 100,
        "accuracy": 79.0,
        "time_taken_min": 150,
        "rank": 340
    },
    {
        "test_name": "Full Mock 4 (Latest)",
        "date": "2026-10-10",
        "score": 76.5,
        "max_score": 100,
        "accuracy": 83.2,
        "time_taken_min": 162,
        "rank": 265
    }
]

TOPIC_MASTERY = [
    {
        "topic": "Algorithms",
        "mastery_score": 88,
        "accuracy": 89.5,
        "benchmark": 75,
        "attempted": 145,
        "status": "Strong",
        "weightage_marks": "9-11"
    },
    {
        "topic": "Data Structures",
        "mastery_score": 85,
        "accuracy": 86.0,
        "benchmark": 75,
        "attempted": 130,
        "status": "Strong",
        "weightage_marks": "7-9"
    },
    {
        "topic": "Operating Systems",
        "mastery_score": 81,
        "accuracy": 82.5,
        "benchmark": 70,
        "attempted": 110,
        "status": "Strong",
        "weightage_marks": "8-10"
    },
    {
        "topic": "Database Systems",
        "mastery_score": 78,
        "accuracy": 79.0,
        "benchmark": 70,
        "attempted": 95,
        "status": "Moderate",
        "weightage_marks": "7-8"
    },
    {
        "topic": "Digital Logic",
        "mastery_score": 74,
        "accuracy": 75.0,
        "benchmark": 65,
        "attempted": 80,
        "status": "Moderate",
        "weightage_marks": "5-6"
    },
    {
        "topic": "Computer Networks",
        "mastery_score": 62,
        "accuracy": 64.0,
        "benchmark": 70,
        "attempted": 105,
        "status": "Needs Work",
        "weightage_marks": "8-10"
    },
    {
        "topic": "Theory of Computation",
        "mastery_score": 54,
        "accuracy": 56.5,
        "benchmark": 72,
        "attempted": 98,
        "status": "Weak",
        "weightage_marks": "8-10"
    },
    {
        "topic": "Compiler Design",
        "mastery_score": 49,
        "accuracy": 51.0,
        "benchmark": 70,
        "attempted": 72,
        "status": "Weak",
        "weightage_marks": "4-6"
    },
    {
        "topic": "Computer Organization",
        "mastery_score": 58,
        "accuracy": 60.0,
        "benchmark": 68,
        "attempted": 85,
        "status": "Needs Work",
        "weightage_marks": "7-9"
    }
]

STRONGEST_TOPICS = [
    {
        "topic": "Algorithms",
        "accuracy": 89.5,
        "mastery": "Expert (88/100)",
        "badge": "Best performing",
        "highlight": "High speed on Dynamic Programming & Divide-and-Conquer"
    },
    {
        "topic": "Data Structures",
        "accuracy": 86.0,
        "mastery": "Proficient (85/100)",
        "badge": "Consistent",
        "highlight": "Flawless on Trees, Heaps, and Hashing"
    },
    {
        "topic": "Operating Systems",
        "accuracy": 82.5,
        "mastery": "Proficient (81/100)",
        "badge": "Reliable",
        "highlight": "Strong on Process Synchronization & Scheduling"
    }
]

WEAKEST_TOPICS = [
    {
        "topic": "Compiler Design",
        "accuracy": 51.0,
        "mastery": "Critical (49/100)",
        "badge": "High negative marking",
        "primary_issue": "Parsing tables (LL(1) & LR(0)/SLR(1)) conflict analysis",
        "negative_marks_lost": 4.66
    },
    {
        "topic": "Theory of Computation",
        "accuracy": 56.5,
        "mastery": "Attention Needed (54/100)",
        "badge": "Concept trap",
        "primary_issue": "Closure properties and Decidability / Undecidability proofs",
        "negative_marks_lost": 6.33
    },
    {
        "topic": "Computer Organization",
        "accuracy": 60.0,
        "mastery": "Improvement Needed (58/100)",
        "badge": "Calculation bottleneck",
        "primary_issue": "Pipelining hazards, branch penalties, and Cache latency calculations",
        "negative_marks_lost": 3.66
    }
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
