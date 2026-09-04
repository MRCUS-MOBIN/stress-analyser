from fastapi import APIRouter
from backend.database import get_database
from backend.services.recovery_service import recovery_service_instance

from visuals.stress_gauge import generate_gauge_data
from visuals.stress_trend import generate_trend_chart_data
from visuals.stress_factors import generate_factors_chart_data
from visuals.stress_fingerprint import generate_stress_fingerprint_data
from visuals.emotion_chart import generate_emotion_chart_data
from visuals.activity_chart import generate_activity_correlation_chart_data
from visuals.recovery_progress import generate_recovery_progress_chart_data
from visuals.recovery_effectiveness import generate_recovery_effectiveness_chart_data

router = APIRouter(prefix="/api/progress", tags=["Visual Analytics Dashboard"])

@router.get("/dashboard/{student_id}")
def get_visual_analytics_dashboard(student_id: str):
    db = get_database()
    assessments = db.find("assessments", {"student_id": student_id}, limit=30)
    recovery_logs = recovery_service_instance.get_student_recovery_history(student_id)
    eff_profile = recovery_service_instance.get_student_effectiveness_profile(student_id)

    latest = assessments[-1] if assessments else {
        "stress_score": 74.5,
        "sleep_hours": 4.5,
        "study_hours": 7.5,
        "screen_time_hours": 7.0,
        "physical_activity_mins": 15.0,
        "academic_workload_score": 8.5,
        "social_activity_hours": 1.5,
        "anxiety_level": 7.5,
        "mood_rating": 4.0,
        "major_factors": [
            {"factor": "Academic Workload & Deadlines", "percentage": 38.5},
            {"factor": "Sleep Deprivation & Disrupted Sleep", "percentage": 32.0},
            {"factor": "Exam & Performance Pressure", "percentage": 18.5},
            {"factor": "Excessive Screen Time", "percentage": 11.0}
        ]
    }

    gauge_data = generate_gauge_data(latest.get("stress_score", 74.5))
    trend_data = generate_trend_chart_data(assessments if assessments else [
        {"date": "Day 1", "stress_score": 52.0},
        {"date": "Day 2", "stress_score": 58.0},
        {"date": "Day 3", "stress_score": 64.0},
        {"date": "Day 4", "stress_score": 61.0},
        {"date": "Day 5", "stress_score": 71.0},
        {"date": "Day 6", "stress_score": 74.5}
    ])
    
    factors_data = generate_factors_chart_data(latest.get("major_factors", [
        {"factor": "Academic Workload & Deadlines", "percentage": 38.5},
        {"factor": "Sleep Deprivation & Disrupted Sleep", "percentage": 32.0},
        {"factor": "Exam & Performance Pressure", "percentage": 18.5},
        {"factor": "Excessive Screen Time", "percentage": 11.0}
    ]))

    fingerprint_data = generate_stress_fingerprint_data(latest)
    emotion_data = generate_emotion_chart_data(latest.get("mood_rating", 4.0), latest.get("anxiety_level", 7.5))
    activity_data = generate_activity_correlation_chart_data(assessments if assessments else [
        {"date": "Day 1", "sleep_hours": 7.0, "study_hours": 4.0, "screen_time_hours": 4.0},
        {"date": "Day 2", "sleep_hours": 6.5, "study_hours": 5.5, "screen_time_hours": 5.0},
        {"date": "Day 3", "sleep_hours": 5.5, "study_hours": 7.0, "screen_time_hours": 6.0},
        {"date": "Day 4", "sleep_hours": 6.0, "study_hours": 6.5, "screen_time_hours": 5.5},
        {"date": "Day 5", "sleep_hours": 5.0, "study_hours": 8.0, "screen_time_hours": 7.0},
        {"date": "Day 6", "sleep_hours": 4.5, "study_hours": 8.5, "screen_time_hours": 7.5}
    ])
    
    recovery_progress_data = generate_recovery_progress_chart_data(recovery_logs)
    recovery_effectiveness_data = generate_recovery_effectiveness_chart_data(eff_profile)

    return {
        "student_id": student_id,
        "latest_score": latest.get("stress_score", 74.5),
        "gauge": gauge_data,
        "trend_chart": trend_data,
        "factors_chart": factors_data,
        "fingerprint_chart": fingerprint_data,
        "emotion_chart": emotion_data,
        "activity_chart": activity_data,
        "recovery_progress_chart": recovery_progress_data,
        "recovery_effectiveness_chart": recovery_effectiveness_data
    }
