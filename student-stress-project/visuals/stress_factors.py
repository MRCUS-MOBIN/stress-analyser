def generate_factors_chart_data(xai_attributions):
    """
    Generates bar chart configuration data for Explainable AI stress factors.
    """
    labels = []
    values = []

    for item in xai_attributions:
        labels.append(item["factor"])
        values.append(item["percentage"])

    return {
        "labels": labels,
        "datasets": [
            {
                "label": "Contributing Factor Percentage (%)",
                "data": values,
                "backgroundColor": [
                    "#ef4444", "#f97316", "#f59e0b", "#8b5cf6", "#3b82f6", "#10b981"
                ],
                "borderRadius": 8
            }
        ]
    }
