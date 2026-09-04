from fastapi import APIRouter
from backend.schemas import RecoveryActionLogSchema
from backend.services.recovery_service import recovery_service_instance
from backend.services.stress_service import stress_service
from backend.database import get_database

router = APIRouter(prefix="/api/recovery", tags=["Personalized Recovery"])

@router.get("/recommendations/{student_id}")
def get_recovery_recommendations(student_id: str):
    db = get_database()
    assessments = db.find("assessments", {"student_id": student_id}, limit=1)
    
    if assessments:
        latest = assessments[-1]
        profile = {
            "stress_nature": latest.get("stress_nature", "Academic"),
            "severity_score": latest.get("stress_score", 70.0),
            "severity_tier": latest.get("severity_tier", "High"),
            "major_factors": [f["factor"] for f in latest.get("major_factors", [])],
            "trajectory": latest.get("stress_trajectory", "Increasing")
        }
    else:
        profile = {
            "stress_nature": "Academic",
            "severity_score": 74.5,
            "severity_tier": "High",
            "major_factors": ["Academic Workload & Deadlines", "Sleep Deprivation"],
            "trajectory": "Increasing"
        }

    return recovery_service_instance.get_personalized_recommendations(student_id, profile)

@router.post("/log")
def log_recovery_action(payload: RecoveryActionLogSchema):
    result = recovery_service_instance.log_recovery_action(
        student_id=payload.student_id,
        activity_id=payload.activity_id,
        activity_title=payload.activity_title,
        pre_stress=payload.pre_stress_score,
        post_stress=payload.post_stress_score,
        duration_mins=payload.duration_mins or 20,
        notes=payload.notes or ""
    )
    return {
        "message": "Recovery action logged and effectiveness profile updated!",
        "log_entry": result,
        "updated_effectiveness_profile": recovery_service_instance.get_student_effectiveness_profile(payload.student_id)
    }

@router.get("/history/{student_id}")
def get_recovery_history(student_id: str):
    logs = recovery_service_instance.get_student_recovery_history(student_id)
    return {
        "student_id": student_id,
        "count": len(logs),
        "logs": logs
    }

@router.get("/effectiveness/{student_id}")
def get_effectiveness_profile(student_id: str):
    profile = recovery_service_instance.get_student_effectiveness_profile(student_id)
    return {
        "student_id": student_id,
        "effectiveness_profile": profile
    }
