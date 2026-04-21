# Civil Engineering Mathematics Assessment Tool

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://civil-eng-maths-assessment.streamlit.app)

A companion assessment platform to the [Engineering Mathematics Toolkit](https://engineering-mathematics-toolkit-atx8ku78wlsyqoqqrzzgew.streamlit.app/), designed specifically for undergraduate civil engineering students. While the Toolkit teaches core mathematical concepts interactively, this app tests applied knowledge, tracks student progress, and gives lecturers actionable cohort insights.

---

## 📌 Overview

Civil engineering students must master mathematics across a wide range of topics — from differential equations modelling structural dynamics to statistics underpinning quality control. This tool bridges the gap between concept learning and applied assessment, using real civil engineering scenarios at three difficulty levels aligned to Ireland's National Framework of Qualifications (NFQ): **L6, L7, and L8**.

---

## 🧰 Features

### 📝 Problem Bank
- 30 civil engineering mathematics problems across 5 topics and 3 NFQ levels
- Filter by topic and difficulty level
- Step-by-step worked solutions revealed on demand
- Common student mistakes highlighted per problem
- Topics include beam deflection, truss analysis, soil consolidation, fluid flow, and structural reliability

### 🎯 Diagnostic Test
- 10-question randomised assessment (2 problems per topic)
- Students self-assess confidence: Confident / Unsure / No Idea
- Interactive radar chart showing topic strength profile on completion
- Personalised recommendations directing weak topics back to the Engineering Mathematics Toolkit

### 📈 Progress Tracker
- Tracks all diagnostic attempts within the session
- Bar chart of problems attempted per topic
- Confidence breakdown per topic (Confident / Unsure / No Idea)
- Motivational summary: strongest topic, weakest topic, total problems attempted

### 🏫 Lecturer Dashboard
- Cohort-level heatmap showing student confidence across all topics
- Ranked list of topics needing most attention
- Traffic light status: Needs Urgent Review / Needs Practice / Doing Well
- Designed for use in lecture planning and targeted intervention

---

## 📐 Mathematics Topics Covered

| Topic | NFQ Levels | Civil Engineering Context |
|---|---|---|
| Calculus | L6, L7, L8 | Road gradients, beam deflection, fluid flow velocity profiles |
| Trigonometry | L6, L7, L8 | Roof pitch, truss force resolution, wind load analysis |
| Linear Algebra | L6, L7, L8 | Material cost systems, coordinate transformation, stiffness matrices |
| Differential Equations | L6, L7, L8 | Drainage rates, concrete cooling, bridge vibration |
| Probability & Statistics | L6, L7, L8 | Concrete strength testing, confidence intervals, structural reliability |

---

## 🚀 Getting Started

### Run Locally

```bash
# Clone the repository
git clone https://github.com/sohumdhole/civil-eng-maths-assessment.git
cd civil-eng-maths-assessment

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Requirements
```
streamlit
plotly
pandas
numpy
scipy
```

---

## 📁 Project Structure

```
civil-eng-maths-assessment/
├── app.py                          # Landing page and session state initialisation
├── problems.json                   # 30 civil engineering mathematics problems
├── requirements.txt
└── pages/
    ├── 1_📝_Problem_Bank.py        # Filterable problem browser
    ├── 2_🎯_Diagnostic_Test.py     # 10-question confidence assessment
    ├── 3_📈_Progress_Tracker.py    # Session progress visualisation
    └── 4_🏫_Lecturer_Dashboard.py  # Cohort analytics dashboard
```

---

## 🔗 Part of a Wider Teaching Platform

This app is one part of a two-app civil engineering mathematics teaching platform:

| App | Purpose | Link |
|---|---|---|
| Engineering Mathematics Toolkit | Interactive concept teaching across 5 modules | [Visit App](https://engineering-mathematics-toolkit-atx8ku78wlsyqoqqrzzgew.streamlit.app/) |
| Civil Eng Maths Assessment Tool | Applied problem bank, diagnostic testing, and cohort analytics | This repository |

Students use the Toolkit to learn and this app to assess. Lecturers use the dashboard to identify where the cohort needs support.

---

## 👨‍💻 Author

**Sohum Dhole**
MSc Business Analytics | BE Electronics Engineering
[GitHub](https://github.com/sohumdhole) · [LinkedIn](https://linkedin.com/in/sohumdhole)
