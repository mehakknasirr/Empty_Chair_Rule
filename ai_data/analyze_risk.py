import pandas as pd

# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

input_file = "ai_data/attendance_dataset.csv"
output_file = "ai_data/risk_analysis.csv"


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
    # STORE STUDENT RESULT
    # --------------------------------------------------

    results.append({

        "student_id": student_id,

        "student_name": student_name,

        "risk_score": risk_score,

        "risk_level": risk_level,

        "trigger_event": trigger_event,

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
# SAVE RISK ANALYSIS
# --------------------------------------------------

risk_df.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("Risk analysis completed successfully!")

print(f"Results saved to: {output_file}")

print("\nStudent Risk Analysis:")

print(
    risk_df[
        [
            "student_id",
            "student_name",
            "risk_score",
            "risk_level",
            "trigger_event"
        ]
    ].to_string(index=False)
)