import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. NEW DATA SCHEMA (Mentor's Concept: Baselines & Pattern Confidence)
DUMMY_DATA = [
    {
      "student_id": "ST101",
      "student_name": "Ali Khan",
      "baseline_attendance": 92.5,  # Personal normal pattern
      "current_attendance": 80.0,   # Recent drop
      "pattern_detected": "Post-Assessment Absence",
      "pattern_confidence": 85,     # Replaced 'risk_score'
      "flag_reason": "Ali has been absent 3 times within 24 hours after major class tests in the last month.",
      "checkin_status": "Pending Check-in",
      "flagged": True
    },
    {
      "student_id": "ST102",
      "student_name": "Sara Ahmed",
      "baseline_attendance": 88.0,
      "current_attendance": 87.5,
      "pattern_detected": "None",
      "pattern_confidence": 15,
      "flag_reason": "Attendance matches personal historical baseline. No significant deviation.",
      "checkin_status": "Not Required",
      "flagged": False
    }
]

# 2. PYDANTIC MODEL FOR HUMAN CHECK-IN
class CheckinRequest(BaseModel):
    student_id: str
    outcome: str
    notes: Optional[str] = None

def load_pattern_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "ai_data", "risk_report.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception:
            return DUMMY_DATA
    return DUMMY_DATA

# 3. GET ENDPOINT (Updated name to align with pattern tracking)
@app.get("/api/pattern-report")
def get_pattern_report():
    return load_pattern_data()

# 4. POST ENDPOINT (New: For Teachers to record outcome)
@app.post("/api/record-checkin")
def record_checkin(request: CheckinRequest):
    # Real app mein yahan database update hoga. 
    # Abhi hum sirf success message return kar rahe hain.
    return {
        "status": "success",
        "message": f"Check-in outcome '{request.outcome}' recorded for student {request.student_id}."
    }