from fastapi import APIRouter
from backend.database import get_database
from backend.services.stress_service import stress_service

router = APIRouter(prefix="/api/stress", tags=["Stress Analysis"])

@router.get("/profile/{student_id}")
def get_latest_stress_profile(student_id: str):
    db = get_database()
    assessments = db.find("assessments", {"student_id": student_id}, limit=1)
    
    if assessments:
        latest = assessments[-1]
        return {
            "student_id": student_id,
            "assessment_id": latest.get("assessment_id", "ASM_001"),
            "severity_score": latest.get("stress_score", 65.0),
            "severity_tier": latest.get("severity_tier", "High"),
            "stress_nature": latest.get("stress_nature", "Academic"),
            "stress_trajectory": latest.get("stress_trajectory", "Increasing"),
            "major_factors": latest.get("major_factors", []),
            "xai_explanation": latest.get("xai_explanation", "Academic workload and sleep deprivation are key drivers."),
            "model_comparisons": latest.get("model_comparisons", {
                "Multimodal_Fusion_DL": 65.0,
                "Random_Forest_Baseline": 63.8,
                "Gradient_Boosting_Baseline": 66.2
            })
        }
    
    # Fallback default profile if no assessments exist
    return {
        "student_id": student_id,
        "assessment_id": "ASM_DEMO",
        "severity_score": 74.5,
        "severity_tier": "High",
        "stress_nature": "Academic",
        "stress_trajectory": "Increasing",
        "major_factors": [
            {"factor": "Academic Workload & Deadlines", "percentage": 38.5, "impact_score": 28.0},
            {"factor": "Sleep Deprivation & Disrupted Sleep", "percentage": 32.0, "impact_score": 23.3},
            {"factor": "Exam & Performance Pressure", "percentage": 18.5, "impact_score": 13.5},
            {"factor": "Excessive Screen Time", "percentage": 11.0, "impact_score": 8.0}
        ],
        "xai_explanation": "The primary driver of stress is Academic Workload & Deadlines (38.5% contribution), followed by Sleep Deprivation (32.0%).",
        "model_comparisons": {
            "Multimodal_Fusion_DL": 74.5,
            "Random_Forest_Baseline": 72.8,
            "Gradient_Boosting_Baseline": 75.2
        }
    }
