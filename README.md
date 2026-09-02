<div align="center">

# 🪑 The Empty Chair Rule

**An AI-powered early risk monitoring system that detects meaningful student absences and engagement drops before grades decline.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🚀 Project Overview

**The Empty Chair Rule** tracks student participation patterns, lab attendances, and submission trends in real-time. Built with a modular architecture, the system provides faculty and academic advisors with actionable insights, risk heatmaps, and automated intervention tools to retain student engagement proactively.

---

## 🛠️ Tech Stack & Architecture

* **Frontend:** Streamlit / Custom Web UI (Dynamic Dashboard with Neon Light/Dark Themes)
* **Backend:** FastAPI (RESTful API & Real-time Stats Engine)
* **Data & Machine Learning:** Python, Pandas, Predictive Analytics & Pattern Recognition

---

## 📂 Repository Structure

```text
EMPTY_CHAIR_RULE/
├── frontend/             # Streamlit dashboard & UI interface
├── backend/              # FastAPI backend services & API endpoints
├── data_analysis/        # ML model scripts & risk pattern reports
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation

⚡ Quick Start Guide
1. Clone the Repository
git clone [https://github.com/mehakknasir/Empty_Chair_Rule.git](https://github.com/mehakknasir/Empty_Chair_Rule.git)
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
✨ Key Features
 Live Roll Call View: Grid chart representing real-time student seating and status.
 Risk Categorization: Dynamic tagging for Critical, Watch, and Stable levels.
 Attendance Trends: Historical pattern visualization using multi-week fill rates.
 Actionable Interventions: Automated advisor alerts, one-click check-ins, and downloadable CSV reports.
🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
📝 License
This project is open-source and available under the MIT License.


