def generate_activity_correlation_chart_data(recent_logs):
    """
    Generates multi-bar correlation chart data comparing Sleep vs. Study vs. Screen Time.
    """
    labels = []
    sleep_data = []
    study_data = []
    screen_data = []

    for idx, item in enumerate(recent_logs):
        labels.append(item.get("date", f"Day {idx+1}"))
        sleep_data.append(round(float(item.get("sleep_hours", 7.0)), 1))
        study_data.append(round(float(item.get("study_hours", 5.0)), 1))
        screen_data.append(round(float(item.get("screen_time_hours", 4.0)), 1))

    return {
        "labels": labels,
        "datasets": [
            {
                "label": "Sleep Hours",
                "data": sleep_data,
                "backgroundColor": "#3b82f6"
            },
            {
                "label": "Study Hours",
                "data": study_data,
                "backgroundColor": "#8b5cf6"
            },
            {
                "label": "Screen Time Hours",
                "data": screen_data,
                "backgroundColor": "#f43f5e"
            }
        ]
    }
