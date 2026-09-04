from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class StudentModel:
    id: str
    name: str
    email: str
    department: str = "Computer Science"
    academic_year: str = "3rd Year"

@dataclass
class DailyAssessmentModel:
    id: str
    student_id: str
    timestamp: str
    sleep_hours: float
    study_hours: float
    screen_time_hours: float
    physical_activity_mins: float
    academic_workload_score: float
    social_activity_hours: float
    anxiety_level: float
    mood_rating: float
    routine_consistency_score: float
    journal_entry: str

@dataclass
class StressProfileModel:
    id: str
    student_id: str
    assessment_id: str
    severity_score: float
    severity_tier: str # Low, Moderate, High, Severe
    stress_nature: str # Academic, Performance, Time-pressure, Sleep-related, Social, Mixed
    stress_trajectory: str # Stable, Increasing, Decreasing, Sudden Escalation
    major_factors: List[Dict]
    xai_explanation: str
    model_comparisons: Dict
