# 🪑 The Empty Chair Rule

> **An AI-powered early risk monitoring system that detects meaningful student absences and engagement drops before grades decline.**

---

## 📌 Project Overview

**The Empty Chair Rule** tracks student participation patterns, lab attendances, and submission trends in real time. Built with a modular architecture, the system provides faculty and academic advisors with actionable insights and automated intervention tools.

---

## 🛠️ Tech Stack & Architecture

* **Frontend:** Streamlit (Interactive Dashboard with Dynamic Light/Dark Themes)
* **Backend:** FastAPI (RESTful API & Real-time Stats Engine)
* **Data & Machine Learning:** Python, Pandas, Predictive Analytics

---

## 📁 Repository Structure

```text
EMPTY_CHAIR_RULE/
├── frontend/             # Streamlit dashboard interface
│   └── app.py
├── backend/              # FastAPI backend services & API endpoints
│   └── main.py
├── data_analysis/        # ML model scripts & risk reports
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation

⚡ Quick Start Guide
1. Clone the Repository
git clone [https://github.com/mehakknasirr/Empty_Chair_Rule.git](https://github.com/mehakknasirr/Empty_Chair_Rule.git)
cd Empty_Chair_Rule

2. Set Up & Run Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Backend server runs at: ⁠http://127.0.0.1:8000⁠

3. Set Up & Run Frontend
cd ../frontend
pip install streamlit requests pandas
streamlit run app.py

Frontend dashboard opens at: ⁠http://localhost:8501⁠

✨ Features
 Live Roll Call View: Grid chart representing real-time student seating and status.
 Risk Categorization: Dynamic tagging for Critical (🚨), Watch (⚠️), and Stable (✓) levels.
 Attendance Trends: Historical pattern visualization using multi-week fill rates.
 Actionable Interventions: Automated advisor alerts and downloadable CSV reports.
