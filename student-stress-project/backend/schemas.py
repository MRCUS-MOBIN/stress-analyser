from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class StudentRegisterSchema(BaseModel):
    name: str = Field(..., example="Alex Morgan")
    email: str = Field(..., example="alex.morgan@university.edu")
    department: Optional[str] = "Computer Science"
    academic_year: Optional[str] = "3rd Year"

class DailyAssessmentSchema(BaseModel):
    student_id: str = Field(default="STU_001")
    sleep_hours: float = Field(..., ge=0.0, le=24.0, example=5.5)
    study_hours: float = Field(..., ge=0.0, le=24.0, example=8.0)
    screen_time_hours: float = Field(..., ge=0.0, le=24.0, example=7.0)
    physical_activity_mins: float = Field(..., ge=0.0, le=300.0, example=15.0)
    academic_workload_score: float = Field(..., ge=1.0, le=10.0, example=8.5)
    social_activity_hours: float = Field(..., ge=0.0, le=24.0, example=1.5)
    anxiety_level: float = Field(..., ge=1.0, le=10.0, example=7.5)
    mood_rating: float = Field(..., ge=1.0, le=10.0, example=4.0)
    routine_consistency_score: float = Field(default=6.0, ge=1.0, le=10.0)
    journal_entry: str = Field(default="", example="Three major midterms coming up this week and I feel anxious.")

class RecoveryActionLogSchema(BaseModel):
    student_id: str = Field(default="STU_001")
    activity_id: str = Field(..., example="rec_box_breathing")
    activity_title: str = Field(..., example="4-7-8 Deep Box Breathing")
    pre_stress_score: float = Field(..., example=75.0)
    post_stress_score: float = Field(..., example=48.0)
    duration_mins: Optional[int] = 15
    notes: Optional[str] = ""

class StressProfileResponseSchema(BaseModel):
    assessment_id: str
    student_id: str
    severity_score: float
    severity_tier: str
    stress_nature: str
    stress_trajectory: str
    major_factors: List[Dict]
    xai_explanation: str
    model_comparisons: Dict
