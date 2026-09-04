from fastapi import APIRouter, HTTPException
from backend.schemas import StudentRegisterSchema
from backend.database import get_database
import uuid

router = APIRouter(prefix="/api/student", tags=["Student Profile"])

@router.post("/register")
def register_student(payload: StudentRegisterSchema):
    db = get_database()
    existing = db.find_one("students", {"email": payload.email})
    if existing:
        return {"message": "Student logged in", "student": existing}

    student_id = f"STU_{uuid.uuid4().hex[:6].upper()}"
    student_doc = {
        "student_id": student_id,
        "name": payload.name,
        "email": payload.email,
        "department": payload.department,
        "academic_year": payload.academic_year
    }

    db.insert_one("students", student_doc)
    return {"message": "Student registered successfully", "student": student_doc}

@router.get("/{student_id}")
def get_student_profile(student_id: str):
    db = get_database()
    student = db.find_one("students", {"student_id": student_id})
    if not student:
        # Default mock student profile for STU_001
        return {
            "student_id": student_id,
            "name": "Alex Morgan",
            "email": "alex.morgan@university.edu",
            "department": "Computer Science & AI",
            "academic_year": "3rd Year"
        }
    return student
