<div align="center">

# 🪑 The Missing Seat

**An AI-powered early risk monitoring system that detects meaningful student absences and engagement drops before grades decline.**

Built for the **Alibaba Cloud Hackathon** 🏆

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20JS-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## 📖 Overview

**The Missing Seat** is an early-warning system that helps educators and academic advisors spot at-risk students before it's too late. By continuously tracking attendance, lab participation, and submission trends, the platform surfaces meaningful drop-offs — not just raw absence counts — and turns them into clear, actionable risk signals.

Powered by a modular backend and a dynamic dashboard, faculty get real-time insight into student engagement instead of discovering problems after grades have already slipped.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🟢 **Real-Time Risk Dashboard** | Live, color-coded view of student engagement status |
| 🚦 **Risk Categorization** | Automated tagging into risk tiers based on attendance and activity patterns |
| 📈 **Predictive Pattern Recognition** | Analytics engine detects early trends before they become failures |
| 🌓 **Neon Light/Dark Dashboard** | Responsive, modern UI built for classroom and admin use |
| 🔔 **Actionable Insights** | Surfaces at-risk students so advisors can intervene early |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, Tailwind CSS, JavaScript — dynamic dashboard with light/dark theming |
| **Backend** | FastAPI — REST API and real-time risk analytics engine |
| **Data & Analytics** | Python, Pandas — predictive analytics and pattern recognition |

---

## 🏗️ Architecture

```
┌───────────────────┐        REST API        ┌──────────────────┐
│    Frontend        │ ─────────────────────▶ │    Backend        │
│  (HTML/CSS/JS)      │ ◀───────────────────── │   (FastAPI)        │
└───────────────────┘                         └──────────────────┘
                                                        │
                                                        ▼
                                              ┌──────────────────┐
                                              │  AI Data Layer     │
                                              │  (Pandas / Risk     │
                                              │   Analysis Engine)  │
                                              └──────────────────┘
```

---

## 📂 Repository Structure

```text
The_Missing_Seat/
├── ai_data/                  # ML datasets, analysis scripts, and risk reports
│   ├── analyze_risk.py
│   ├── attendance_dataset.csv
│   ├── generate_dataset.py
│   ├── risk_analysis.csv
│   └── risk_report.json
├── backend/                  # FastAPI backend services & API endpoints
│   ├── main.py
│   └── requirements.txt
├── frontend/                 # Interactive web dashboard
│   └── missing_seat_ui/
│       ├── index.html
│       ├── script.js
│       └── style.css
├── .gitignore
├── LICENSE                   # MIT License
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/mehakknasir/The_Missing_Seat.git
cd The_Missing_Seat
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend API available at: **http://127.0.0.1:8000**

### 3. Frontend Launch
Simply open `frontend/missing_seat_ui/index.html` in any browser, or launch it via VS Code's **Live Server** extension for hot-reload during development.

---

## 🖥️ Usage

1. Start the FastAPI backend to power the risk analytics engine and API endpoints.
2. Open the dashboard to view real-time student engagement and risk status.
3. Review students flagged as at-risk and take early action through advisor outreach.
4. Use the underlying datasets in `ai_data/` to retrain or fine-tune the risk model as needed.

---

## 🗺️ Roadmap

- [ ] Deploy on Alibaba Cloud (ECS / Function Compute)
- [ ] Integrate with existing LMS platforms (Canvas, Moodle)
- [ ] Add configurable risk-scoring thresholds per institution
- [ ] Email/SMS notification channel for advisors
- [ ] Role-based access control for faculty vs. administrators

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/mehakknasir/The_Missing_Seat/issues) or open a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

---

<div align="center">


