def generate_recovery_effectiveness_chart_data(student_effectiveness_profile):
    """
    Generates horizontal bar chart ranking recovery strategies by personalized efficiency score.
    """
    labels = []
    scores = []

    # Default fallback strategies if no logs exist yet
    default_items = [
        ("4-7-8 Deep Box Breathing", 92.0),
        ("90-Min Bedtime Digital Detox", 88.5),
        ("Pomodoro Study & Rest Routine", 84.0),
        ("30-Min Cardio Exercise", 82.0)
    ]

    if student_effectiveness_profile:
        for act_id, info in student_effectiveness_profile.items():
            if isinstance(info, dict):
                labels.append(info.get("activity_title", act_id))
                scores.append(float(info.get("effectiveness_score", 75.0)))
            else:
                title = act_id.replace("rec_", "").replace("_", " ").title()
                labels.append(title)
                scores.append(float(info))
    else:
        for title, score in default_items:
            labels.append(title)
            scores.append(score)

    return {
        "labels": labels,
        "datasets": [
            {
                "label": "Personal Effectiveness Rating (%)",
                "data": scores,
                "backgroundColor": "#6366f1",
                "borderRadius": 6
            }
        ]
    }
