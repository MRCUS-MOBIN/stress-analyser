def generate_stress_fingerprint_data(assessment_data):
    """
    Generates a multi-axis Radar Chart (Stress Fingerprint) comparing 6 core dimensions:
    Academic Load, Sleep Deficit, Anxiety Level, Screen Exposure, Exercise Deficit, Social Isolation.
    """
    sleep = float(assessment_data.get("sleep_hours", 7.0))
    workload = float(assessment_data.get("academic_workload_score", 5.0))
    anxiety = float(assessment_data.get("anxiety_level", 5.0))
    screen = float(assessment_data.get("screen_time_hours", 4.0))
    activity = float(assessment_data.get("physical_activity_mins", 30.0))
    social = float(assessment_data.get("social_activity_hours", 3.0))

    sleep_deficit = min(10.0, max(0.0, (8.0 - sleep) * 2.0))
    academic_load = min(10.0, workload)
    anxiety_score = min(10.0, anxiety)
    screen_exposure = min(10.0, (screen / 10.0) * 10.0)
    exercise_deficit = min(10.0, max(0.0, (45.0 - activity) / 4.5))
    social_isolation = min(10.0, max(0.0, (5.0 - social) * 2.0))

    categories = [
        "Academic Load", "Sleep Deficit", "Anxiety Level",
        "Screen Exposure", "Exercise Deficit", "Social Isolation"
    ]
    student_scores = [
        round(academic_load, 1),
        round(sleep_deficit, 1),
        round(anxiety_score, 1),
        round(screen_exposure, 1),
        round(exercise_deficit, 1),
        round(social_isolation, 1)
    ]
    ideal_scores = [3.0, 1.0, 2.0, 2.5, 1.0, 1.5]

    return {
        "labels": categories,
        "datasets": [
            {
                "label": "Student Stress Fingerprint",
                "data": student_scores,
                "backgroundColor": "rgba(239, 68, 68, 0.25)",
                "borderColor": "#ef4444",
                "pointBackgroundColor": "#ef4444"
            },
            {
                "label": "Healthy Benchmark",
                "data": ideal_scores,
                "backgroundColor": "rgba(16, 185, 129, 0.15)",
                "borderColor": "#10b981",
                "pointBackgroundColor": "#10b981"
            }
        ]
    }
