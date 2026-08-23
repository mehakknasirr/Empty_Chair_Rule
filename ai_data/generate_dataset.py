import pandas as pd
import random
from datetime import date, timedelta

# Student information
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

# Possible day events
events = [
    "Normal_Day",
    "Post_Test",
    "Post_Holiday",
    "Post_PTM"
]

# Generate dates
start_date = date(2026, 1, 1)
number_of_days = 90

data = []

for day in range(number_of_days):
    current_date = start_date + timedelta(days=day)

    # Randomly assign an event to each day
    day_event = random.choices(
        events,
        weights=[70, 10, 10, 10]
    )[0]

    for student_id, student_name in students:

        # Create realistic attendance patterns
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

# Create DataFrame
df = pd.DataFrame(data)

# Save CSV inside ai_data
output_file = "ai_data/attendance_dataset.csv"
df.to_csv(output_file, index=False)

print(f"Dataset generated successfully!")
print(f"Rows: {len(df)}")
print(f"Saved to: {output_file}")
print("\nColumns:")
print(df.columns.tolist())