def generate_recovery_progress_chart_data(recovery_logs):
    """
    Generates Pre vs. Post Intervention Stress Comparison bar chart data.
    """
    labels = []
    pre_scores = []
    post_scores = []

    for item in recovery_logs[-6:]: # Last 6 intervention logs
        title_short = item.get("activity_title", "Intervention")[:18] + "..."
        labels.append(title_short)
        pre_scores.append(round(float(item.get("pre_stress_score", 70.0)), 1))
        post_scores.append(round(float(item.get("post_stress_score", 45.0)), 1))

    return {
        "labels": labels if labels else ["Box Breathing", "Digital Detox", "Pomodoro Break"],
        "datasets": [
            {
                "label": "Pre-Intervention Stress",
                "data": pre_scores if pre_scores else [78.0, 82.0, 68.0],
                "backgroundColor": "#ef4444"
            },
            {
                "label": "Post-Intervention Stress",
                "data": post_scores if post_scores else [52.0, 58.0, 42.0],
                "backgroundColor": "#10b981"
            }
        ]
    }
