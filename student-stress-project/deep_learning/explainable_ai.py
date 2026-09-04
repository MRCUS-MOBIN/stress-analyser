import numpy as np

class ExplainableAIEngine:
    """
    Explainable AI (XAI) component that computes percentage feature attributions 
    and key contributing factors for a student's stress prediction.
    """
    def __init__(self):
        self.feature_weights = {
            "sleep_deprivation": {"weight": 0.28, "label": "Sleep Deprivation & Poor Sleep Quality", "threshold": 6.5, "direction": "below"},
            "academic_workload": {"weight": 0.25, "label": "High Academic Workload & Deadlines", "threshold": 6.0, "direction": "above"},
            "exam_anxiety": {"weight": 0.20, "label": "Exam & Performance Anxiety", "threshold": 5.5, "direction": "above"},
            "screen_time": {"weight": 0.12, "label": "Excessive Late-night Screen Time", "threshold": 6.5, "direction": "above"},
            "low_activity": {"weight": 0.08, "label": "Lack of Physical Exercise", "threshold": 25.0, "direction": "below"},
            "social_isolation": {"weight": 0.07, "label": "Social Strain & Low Interaction", "threshold": 2.0, "direction": "below"}
        }

    def explain_stress_prediction(self, assessment_data, predicted_severity):
        """
        Calculates feature attributions and returns structured XAI breakdown.
        """
        sleep = float(assessment_data.get("sleep_hours", 7.0))
        workload = float(assessment_data.get("academic_workload_score", 5.0))
        anxiety = float(assessment_data.get("anxiety_level", 5.0))
        screen = float(assessment_data.get("screen_time_hours", 4.0))
        activity = float(assessment_data.get("physical_activity_mins", 30.0))
        social = float(assessment_data.get("social_activity_hours", 3.0))

        contributions = {}
        
        # 1. Sleep impact
        if sleep < 6.5:
            contributions["Sleep Deprivation & Disrupted Sleep"] = round((6.5 - sleep) * 8.5 + 10.0, 1)
        else:
            contributions["Sleep Deprivation & Disrupted Sleep"] = 5.0

        # 2. Academic Workload impact
        if workload > 5.5:
            contributions["Academic Workload & Deadlines"] = round((workload - 5.5) * 8.0 + 12.0, 1)
        else:
            contributions["Academic Workload & Deadlines"] = 6.0

        # 3. Anxiety impact
        if anxiety > 5.0:
            contributions["Exam & Performance Pressure"] = round((anxiety - 5.0) * 7.5 + 10.0, 1)
        else:
            contributions["Exam & Performance Pressure"] = 5.0

        # 4. Screen time impact
        if screen > 6.0:
            contributions["Excessive Screen Time"] = round((screen - 6.0) * 5.0 + 8.0, 1)
        else:
            contributions["Excessive Screen Time"] = 4.0

        # 5. Low physical activity impact
        if activity < 30.0:
            contributions["Lack of Physical Activity"] = round((30.0 - activity) * 0.4 + 6.0, 1)
        else:
            contributions["Lack of Physical Activity"] = 3.0

        # 6. Social activity impact
        if social < 2.0:
            contributions["Social Strain & Isolation"] = round((2.0 - social) * 6.0 + 7.0, 1)
        else:
            contributions["Social Strain & Isolation"] = 4.0

        total_raw = sum(contributions.values())
        
        # Normalize to 100%
        normalized_attributions = []
        for factor, val in contributions.items():
            percentage = round((val / total_raw) * 100.0, 1)
            normalized_attributions.append({
                "factor": factor,
                "percentage": percentage,
                "impact_score": round(val, 1)
            })

        # Sort descending by contribution
        normalized_attributions.sort(key=lambda x: x["percentage"], reverse=True)

        top_contributor = normalized_attributions[0]["factor"]
        
        explanation_summary = f"The primary driver of stress is {top_contributor} ({normalized_attributions[0]['percentage']}% contribution), followed by {normalized_attributions[1]['factor']} ({normalized_attributions[1]['percentage']}%)."

        return {
            "top_contributor": top_contributor,
            "summary": explanation_summary,
            "attributions": normalized_attributions
        }

if __name__ == "__main__":
    xai = ExplainableAIEngine()
    sample_data = {
        "sleep_hours": 4.5,
        "academic_workload_score": 8.5,
        "anxiety_level": 7.5,
        "screen_time_hours": 8.0,
        "physical_activity_mins": 10.0,
        "social_activity_hours": 1.0
    }
    result = xai.explain_stress_prediction(sample_data, predicted_severity=78.5)
    print("XAI Summary:", result["summary"])
    print("Factor Attributions:", result["attributions"])
