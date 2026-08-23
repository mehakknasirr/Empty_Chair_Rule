import pandas as pd
import json

# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

input_file = "ai_data/attendance_dataset.csv"
csv_output_file = "ai_data/risk_analysis.csv"
json_output_file = "ai_data/risk_report.json"


# --------------------------------------------------
# LOAD ATTENDANCE DATA
# --------------------------------------------------

df = pd.read_csv(input_file)


# --------------------------------------------------
# ANALYZE EACH STUDENT
# --------------------------------------------------

results = []

for student_id in df["student_id"].unique():

    student_df = df[df["student_id"] == student_id]

    student_name = student_df["student_name"].iloc[0]

    # --------------------------------------------------
    # OVERALL ABSENCE RATE
    # --------------------------------------------------

    total_days = len(student_df)

    total_absences = (
        student_df["attendance_status"] == "Absent"
    ).sum()

    overall_absence_rate = total_absences / total_days


    # --------------------------------------------------
    # NORMAL DAY ABSENCE RATE
    # --------------------------------------------------

    normal_days = student_df[
        student_df["day_event"] == "Normal_Day"
    ]

    if len(normal_days) > 0:
        normal_absence_rate = (
            normal_days["attendance_status"] == "Absent"
        ).mean()
    else:
        normal_absence_rate = 0


    # --------------------------------------------------
    # EVENT-SPECIFIC ABSENCE RATES
    # --------------------------------------------------

    event_rates = {}

    for event in [
        "Post_Test",
        "Post_Holiday",
        "Post_PTM"
    ]:

        event_days = student_df[
            student_df["day_event"] == event
        ]

        if len(event_days) > 0:

            absence_rate = (
                event_days["attendance_status"] == "Absent"
            ).mean()

        else:

            absence_rate = 0

        event_rates[event] = absence_rate


    # --------------------------------------------------
    # FIND STRONGEST TRIGGER
    # --------------------------------------------------

    strongest_event = max(
        event_rates,
        key=event_rates.get
    )

    strongest_rate = event_rates[strongest_event]


    # --------------------------------------------------
    # COUNT ABSENCES FOR STRONGEST EVENT
    # --------------------------------------------------

    strongest_event_days = student_df[
        student_df["day_event"] == strongest_event
    ]

    strongest_event_absences = (
        strongest_event_days["attendance_status"] == "Absent"
    ).sum()


    # --------------------------------------------------
    # PATTERN STRENGTH
    # --------------------------------------------------

    # Compare event-related absence with
    # the student's normal absence rate.

    pattern_strength = max(
        0,
        strongest_rate - normal_absence_rate
    )


    # --------------------------------------------------
    # RISK SCORE
    # --------------------------------------------------

    # Event-related pattern = 75% of score
    # Overall absence = 25% of score

    event_score = pattern_strength * 100

    overall_score = overall_absence_rate * 100

    risk_score = (
        event_score * 0.75
        + overall_score * 0.25
    )

    # Keep score between 0 and 100
    risk_score = round(
        min(100, max(0, risk_score))
    )


    # --------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------

    if risk_score >= 60:
        risk_level = "High"

    elif risk_score >= 30:
        risk_level = "Medium"

    else:
        risk_level = "Low"


    # --------------------------------------------------
    # TRIGGER EVENT
    # --------------------------------------------------

    trigger_names = {
        "Post_Test": "Absent after Test",
        "Post_Holiday": "Absent after Holiday",
        "Post_PTM": "Absent after PTM"
    }

    if pattern_strength > 0:

        trigger_event = trigger_names[strongest_event]

    else:

        trigger_event = "None"


    # --------------------------------------------------
    # NATURAL LANGUAGE SUMMARY
    # --------------------------------------------------

    if risk_level in ["Medium", "High"]:

        if strongest_event == "Post_Test":
            summary = (
                f"{student_name} was absent "
                f"{strongest_event_absences} times after tests"
            )

        elif strongest_event == "Post_Holiday":
            summary = (
                f"{student_name} was absent "
                f"{strongest_event_absences} times after holidays"
            )

        elif strongest_event == "Post_PTM":
            summary = (
                f"{student_name} was absent "
                f"{strongest_event_absences} times after PTM days"
            )

        else:
            summary = (
                f"{student_name} has an elevated attendance risk"
            )

    else:

        summary = ""


    # --------------------------------------------------
    # FLAGGED STATUS
    # --------------------------------------------------

    flagged = risk_level in ["Medium", "High"]


    # --------------------------------------------------
    # STORE FULL ANALYSIS RESULT
    # --------------------------------------------------

    results.append({

        "student_id": student_id,

        "student_name": student_name,

        "risk_score": risk_score,

        "risk_level": risk_level,

        "trigger_event": trigger_event,

        "summary": summary,

        "flagged": flagged,

        "overall_absence_rate": round(
            overall_absence_rate * 100,
            2
        ),

        "normal_absence_rate": round(
            normal_absence_rate * 100,
            2
        ),

        "post_test_absence_rate": round(
            event_rates["Post_Test"] * 100,
            2
        ),

        "post_holiday_absence_rate": round(
            event_rates["Post_Holiday"] * 100,
            2
        ),

        "post_ptm_absence_rate": round(
            event_rates["Post_PTM"] * 100,
            2
        )
    })


# --------------------------------------------------
# CREATE RESULT DATAFRAME
# --------------------------------------------------

risk_df = pd.DataFrame(results)


# --------------------------------------------------
# SAVE CSV FOR ANALYSIS / DEBUGGING
# --------------------------------------------------

risk_df.to_csv(
    csv_output_file,
    index=False
)


# --------------------------------------------------
# CREATE FINAL BACKEND JSON
# --------------------------------------------------

risk_report = []

for result in results:

    risk_report.append({
        "student_id": result["student_id"],
        "student_name": result["student_name"],
        "risk_score": result["risk_score"],
        "risk_level": result["risk_level"],
        "summary": result["summary"],
        "flagged": result["flagged"]
    })


# --------------------------------------------------
# SAVE JSON
# --------------------------------------------------

with open(
    json_output_file,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        risk_report,
        file,
        indent=2
    )


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("Risk analysis completed successfully!")

print(f"CSV saved to: {csv_output_file}")
print(f"JSON saved to: {json_output_file}")

print("\nStudent Risk Analysis:")

print(
    risk_df[
        [
            "student_id",
            "student_name",
            "risk_score",
            "risk_level",
            "summary",
            "flagged"
        ]
    ].to_string(index=False)
)