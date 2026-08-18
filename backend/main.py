import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DUMMY_DATA = [
    {
      "student_id": "ST101",
      "student_name": "Ali Khan",
      "risk_score": 85,
      "risk_level": "High",
      "summary": "Absent 3 times right after class tests",
      "flagged": True
    },
    {
      "student_id": "ST102",
      "student_name": "Sara Ahmed",
      "risk_score": 20,
      "risk_level": "Low",
      "summary": "Normal attendance",
      "flagged": False
    }
]

def load_risk_data():
    # Check if Rehan's generated JSON file exists in /ai_data folder
    file_path = os.path.join("..", "ai_data", "risk_report.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception:
            return DUMMY_DATA
    return DUMMY_DATA

@app.get("/")
def home():
    return {"message": "Empty Chair Rule API is running!"}

@app.get("/api/students/risk-report")
def get_risk_report():
    return load_risk_data()

# Nayi API top dashboard cards ke liye (Total, High Risk, Medium Risk counts)
@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    data = load_risk_data()
    total_students = len(data)
    high_risk_count = sum(1 for s in data if s.get("risk_level") == "High")
    medium_risk_count = sum(1 for s in data if s.get("risk_level") == "Medium")
    
    return {
        "total_students": total_students,
        "high_risk_count": high_risk_count,
        "medium_risk_count": medium_risk_count
    }
