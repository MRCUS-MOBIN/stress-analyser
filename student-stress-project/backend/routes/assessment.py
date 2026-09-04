from fastapi import APIRouter
from backend.schemas import DailyAssessmentSchema
from backend.database import get_database
from backend.services.stress_service import stress_service
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/assessment", tags=["Assessment"])

@router.post("/submit")
def submit_assessment(payload: DailyAssessmentSchema):
    db = get_database()
    student_id = payload.student_id or "STU_001"

    # Fetch historical assessments for sequence modeling
    history = db.find("assessments", {"student_id": student_id}, limit=10)

    assessment_dict = payload.dict()
    
    # Run Multimodal Deep Learning & Explainable AI analysis
    profile = stress_service.analyze_assessment(assessment_dict, historical_assessments=history)

    assessment_id = f"ASM_{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.now().isoformat()

    doc = {
        "assessment_id": assessment_id,
        "student_id": student_id,
        "timestamp": timestamp,
        **assessment_dict,
        "stress_score": profile["severity_score"],
        "severity_tier": profile["severity_tier"],
        "stress_nature": profile["stress_nature"],
        "stress_trajectory": profile["stress_trajectory"],
        "major_factors": profile["major_factors"],
        "xai_explanation": profile["xai_explanation"],
        "model_comparisons": profile["model_comparisons"]
    }

    db.insert_one("assessments", doc)

    return {
        "message": "Assessment submitted and analyzed successfully",
        "assessment_id": assessment_id,
        "stress_profile": profile
    }

@router.get("/history/{student_id}")
def get_assessment_history(student_id: str):
    db = get_database()
    items = db.find("assessments", {"student_id": student_id}, limit=30)
    return {"student_id": student_id, "count": len(items), "history": items}
