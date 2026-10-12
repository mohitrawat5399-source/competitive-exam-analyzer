# 🎯 Competitive Exam Analyzer & Practice Suite (GATE CS)

A modern, high-performance Streamlit web application designed to help competitive exam aspirants (specifically **GATE Computer Science & Engineering**) analyze performance trends, practice real exam-style questions with interactive timers, diagnose topic-level weaknesses, and follow personalized revision roadmaps.

---

## 🌟 Key Features

### 1. 📊 Interactive Dashboard (Landing Page)
- **High-Impact Metric Cards**: Real-time display of Average Mock Score, Accuracy Rate, Total Tests Taken, and Estimated Percentile.
- **Performance Progression Chart**: Interactive Plotly time-series chart tracking score and accuracy across mock tests alongside the IIT cutoff benchmark (70 marks).
- **Strongest vs Weakest Topics**: Visual categorization of subjects with accuracy percentages, mastery tiers, and negative-mark impact flags.
- **Prominent Start Practice Action**: Instant one-click CTA to launch practice sessions immediately.

### 2. ✍️ Practice Arena
- **Exam & Topic Filtering**: Filter by target exam (GATE CS), question year (2021–2024 PYQs), or specific topics (Algorithms, OS, TOC, Networks, DBMS, etc.).
- **Authentic Question Bank**: Realistic GATE CS multiple-choice questions with LaTeX mathematical equations.
- **Exam Simulation Controls**:
  - Live session countdown timer.
  - Question navigation palette with color indicators (Answered, Current, Marked for Review, Unvisited).
  - Navigation controls: `Previous`, `Next`, `Mark for Review`, `Clear Choice`.
  - **Instant Submission & Evaluation**: Immediate score calculation (+marks for correct, negative penalty for incorrect), accuracy percentage, and in-depth step-by-step solutions.

### 3. 📈 In-Depth Analysis & Diagnostics
- **Sample Score & Accuracy Summary**: Connected directly to your practice session or benchmark mocks.
- **Topic Mastery Comparison Chart**: Visual benchmark comparison contrasting your accuracy against topper cutoffs across all GATE CS core topics.
- **Weak-Topic Diagnostics**: Identification of negative-marking leakages, conceptual traps, and calculation bottlenecks.
- **Actionable Revision Roadmap**: Prioritized study targets (High / Medium / Maintenance) with suggested problem counts and a revision checklist.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ installed

### Installation & Run

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application**:
   ```bash
   streamlit run main.py
   ```

4. **Access the application**:
   Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```text
competitive-exam-analyzer/
├── main.py                  # Main entry point & routing
├── styles.py                # Custom CSS theme & card styling
├── requirements.txt         # Project dependencies
├── components/
│   ├── __init__.py
│   ├── dashboard_view.py    # Dashboard landing page
│   ├── practice_view.py     # Practice arena & question simulation
│   └── analysis_view.py     # Diagnostic analytics & revision plans
└── data/
    ├── questions.py         # Curated GATE CS questions database
    └── mock_history.py      # Historical mock scores and mastery benchmarks
```
