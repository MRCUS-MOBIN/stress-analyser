def generate_emotion_chart_data(mood_rating, anxiety_level, text_journal=""):
    """
    Generates doughnut chart metrics for Mood, Emotion & Sentiment Distribution.
    """
    mood = float(mood_rating)
    anxiety = float(anxiety_level)

    positive_sentiment = max(5.0, min(95.0, (mood / 10.0) * 80.0))
    anxiety_sentiment = max(5.0, min(90.0, (anxiety / 10.0) * 75.0))
    calm_neutral = max(0.0, 100.0 - (positive_sentiment + anxiety_sentiment))

    return {
        "labels": ["Positive / Optimistic", "Anxious / Overwhelmed", "Calm / Neutral"],
        "datasets": [
            {
                "data": [round(positive_sentiment, 1), round(anxiety_sentiment, 1), round(calm_neutral, 1)],
                "backgroundColor": ["#10b981", "#ef4444", "#64748b"]
            }
        ]
    }
