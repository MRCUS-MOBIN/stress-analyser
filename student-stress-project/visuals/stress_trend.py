def generate_trend_chart_data(historical_assessments):
    """
    Generates historical line chart data for stress trajectory over days.
    """
    labels = []
    scores = []
    baseline_thresholds = []

    for idx, item in enumerate(historical_assessments):
        day_label = item.get("date", f"Day {idx + 1}")
        labels.append(day_label)
        scores.append(round(float(item.get("stress_score", 50.0)), 1))
        baseline_thresholds.append(50.0) # Normal stress threshold line

    return {
        "labels": labels,
        "datasets": [
            {
                "label": "Student Stress Trajectory",
                "data": scores,
                "borderColor": "#6366f1",
                "backgroundColor": "rgba(99, 102, 241, 0.15)",
                "fill": True,
                "tension": 0.4
            },
            {
                "label": "Optimal Threshold (50)",
                "data": baseline_thresholds,
                "borderColor": "#10b981",
                "borderDash": [5, 5],
                "fill": False
            }
        ]
    }
