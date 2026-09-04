def generate_gauge_data(severity_score):
    """
    Generates configuration data for the Stress Severity Gauge widget.
    """
    score = float(severity_score)
    if score < 35.0:
        label = "Low Stress"
        color = "#10b981" # Emerald Green
        level_class = "low"
    elif score < 60.0:
        label = "Moderate Stress"
        color = "#f59e0b" # Amber Yellow
        level_class = "moderate"
    elif score < 80.0:
        label = "High Stress"
        color = "#f97316" # Bright Orange
        level_class = "high"
    else:
        label = "Severe Stress"
        color = "#ef4444" # Crimson Red
        level_class = "severe"

    return {
        "score": round(score, 1),
        "max_score": 100.0,
        "label": label,
        "color": color,
        "level_class": level_class,
        "needle_angle_deg": round((score / 100.0) * 180.0 - 90.0, 1)
    }

if __name__ == "__main__":
    print(generate_gauge_data(74.5))
