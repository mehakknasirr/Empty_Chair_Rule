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
    file_path = os.path.join(os.path.dirname(__file__), "..", "ai_data", "risk_report.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception:
            return DUMMY_DATA
    return DUMMY_DATA

@app.get("/api/risk-report")
def get_risk_report():
    return load_risk_data()
