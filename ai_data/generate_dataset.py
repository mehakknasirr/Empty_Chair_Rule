import pandas as pd
import random
from datetime import date, timedelta

# Make the dataset reproducible
random.seed(42)

# --------------------------------------------------
# STUDENT INFORMATION
# --------------------------------------------------

students = [
    ("ST001", "Ali Khan"),
    ("ST002", "Ahmed Raza"),
    ("ST003", "Sara Ahmed"),
    ("ST004", "Hassan Ali"),
    ("ST005", "Ayesha Khan"),
    ("ST006", "Usman Malik"),
    ("ST007", "Fatima Noor"),
    ("ST008", "Hamza Shah"),
    ("ST009", "Zainab Iqbal"),
    ("ST010", "Bilal Ahmed"),
]

# --------------------------------------------------
# DAY EVENTS
# --------------------------------------------------

events = (
    ["Normal_Day"] * 63
    + ["Post_Test"] * 9
    + ["Post_Holiday"] * 9
    + ["Post_PTM"] * 9
)

# Shuffle the event dates
random.shuffle(events)

# --------------------------------------------------
# INTENTIONAL STUDENT PATTERNS
# --------------------------------------------------

risk_patterns = {
    "ST003": "Post_Test",
    "ST007": "Post_Holiday",
    "ST009": "Post_PTM"
}

# --------------------------------------------------
# GENERATE DATA
# --------------------------------------------------

start_date = date(2026, 1, 1)
data = []

for day in range(90):

    current_date = start_date + timedelta(days=day)
    day_event = events[day]

    for student_id, student_name in students:

        # ------------------------------------------
        # INTENTIONAL PATTERN STUDENTS
        # ------------------------------------------

        if student_id in risk_patterns:

            trigger_event = risk_patterns[student_id]

            if day_event == trigger_event:
                # Deliberately create a strong pattern
                attendance_status = "Absent"
            else:
                # Normal attendance on other days
                attendance_status = random.choices(
                    ["Present", "Absent"],
                    weights=[90, 10]
                )[0]

        # ------------------------------------------
        # NORMAL STUDENTS
        # ------------------------------------------

        else:

            if day_event == "Post_Test":
                attendance_status = random.choices(
                    ["Present", "Absent"],
                    weights=[65, 35]
                )[0]

            elif day_event == "Post_Holiday":
                attendance_status = random.choices(
                    ["Present", "Absent"],
                    weights=[70, 30]
                )[0]

            elif day_event == "Post_PTM":
                attendance_status = random.choices(
                    ["Present", "Absent"],
                    weights=[75, 25]
                )[0]

            else:
                attendance_status = random.choices(
                    ["Present", "Absent"],
                    weights=[90, 10]
                )[0]

        data.append({
            "student_id": student_id,
            "student_name": student_name,
            "date": current_date,
            "attendance_status": attendance_status,
            "day_event": day_event
        })

# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(data)

# --------------------------------------------------
# SAVE CSV
# --------------------------------------------------

output_file = "ai_data/attendance_dataset.csv"
df.to_csv(output_file, index=False)

# --------------------------------------------------
# DISPLAY INFORMATION
# --------------------------------------------------

print("Dataset generated successfully!")
print(f"Rows: {len(df)}")
print(f"Saved to: {output_file}")

print("\nColumns:")
print(df.columns.tolist())

print("\nDay event distribution:")
print(df["day_event"].value_counts())

print("\nIntentional patterns:")
for student_id, event in risk_patterns.items():
    print(f"{student_id}: Absent after {event}")