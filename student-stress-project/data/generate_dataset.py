import os
import json
import random
import numpy as np
import pandas as pd

def generate_student_dataset(num_students=80, days_per_student=7, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    journal_templates = {
        "Academic": [
            "I have three major midterms coming up this week and I feel completely unprepared.",
            "Struggling with the heavy assignment load and complex programming projects.",
            "Can't focus on studying due to overwhelming course requirements and deadlines.",
            "Extremely anxious about upcoming lab exams and pending submissions."
        ],
        "Performance": [
            "Terrified about campus placement interviews and job application rejections.",
            "Constant pressure to perform well and keep up high GPA expectations.",
            "Worried about my upcoming seminar presentation in front of professors.",
            "Feeling inadequate compared to my peers during coding competitive tests."
        ],
        "Time-pressure": [
            "Running out of time to complete all my tasks today, constantly rushing.",
            "Too many deadlines overlapping on the same day, feeling breathless.",
            "Poor time management has left me pulling late nights to meet project milestones.",
            "Juggling classes, projects, and personal commitments is overwhelming."
        ],
        "Sleep-related": [
            "Insomnia is killing me. Only slept 3 hours last night and feel exhausted.",
            "Disrupted sleep schedule and constant headaches throughout the morning.",
            "Waking up feeling tired despite sleeping late, unable to get restful sleep.",
            "Screen usage late at night is ruining my sleep quality."
        ],
        "Social": [
            "Feeling isolated from my peer group and struggling with campus social life.",
            "Had a conflict with roommate and feeling socially strained.",
            "Missing home and feeling lonely during weekends in the college dormitory.",
            "Difficulty balancing group project communication and team dynamics."
        ],
        "Mixed": [
            "Everything is building up at once - exams, poor sleep, and placement worries.",
            "Exhausted from constant workload, lack of sleep, and social fatigue.",
            "Feeling overwhelmed by academic deadlines and personal life stress.",
            "Struggling to manage daily routine, exams, and keeping up health."
        ]
    }

    records = []
    
    for s_idx in range(1, num_students + 1):
        student_id = f"STU_{s_idx:03d}"
        
        # Primary stress persona for student
        primary_nature = random.choice(["Academic", "Performance", "Time-pressure", "Sleep-related", "Social", "Mixed"])
        base_trend = random.choice(["Stable", "Increasing", "Decreasing", "Sudden Escalation"])
        
        base_sleep = random.uniform(4.5, 8.5)
        base_study = random.uniform(3.0, 9.0)
        base_screen = random.uniform(3.0, 8.0)
        base_activity = random.uniform(15, 60)
        base_workload = random.uniform(3.0, 9.0)
        base_social = random.uniform(1.0, 5.0)

        for d in range(1, days_per_student + 1):
            # Apply trend drift
            drift = (d - 1) * 0.15 if base_trend == "Increasing" else (-(d - 1) * 0.15 if base_trend == "Decreasing" else 0)
            if base_trend == "Sudden Escalation" and d >= 5:
                drift += 1.5

            if primary_nature == "Academic":
                workload = min(10.0, max(2.0, base_workload + drift + random.uniform(0.5, 1.5)))
                sleep = min(9.0, max(3.5, base_sleep - drift * 0.5 - random.uniform(0.2, 0.8)))
                study = min(12.0, max(2.0, base_study + random.uniform(0.5, 2.0)))
                screen = min(10.0, max(2.0, base_screen + random.uniform(0, 1.0)))
                activity = max(5, base_activity - random.uniform(0, 15))
                social = max(0.5, base_social - random.uniform(0, 1.0))
                anxiety = min(10.0, max(2.0, 5.5 + workload * 0.4 - sleep * 0.3))
                mood = max(1.0, min(10.0, 8.0 - anxiety * 0.5))
            elif primary_nature == "Sleep-related":
                sleep = min(9.0, max(2.5, 4.0 - drift + random.uniform(-0.5, 0.5)))
                screen = min(12.0, max(4.0, 7.5 + random.uniform(0.5, 2.0)))
                workload = min(10.0, max(2.0, base_workload + random.uniform(-0.5, 0.5)))
                study = min(10.0, max(2.0, base_study))
                activity = max(0, base_activity - random.uniform(10, 20))
                social = max(0.5, base_social)
                anxiety = min(10.0, max(2.0, 6.0 + (7 - sleep) * 0.5))
                mood = max(1.0, min(10.0, sleep * 0.9))
            elif primary_nature == "Performance":
                workload = min(10.0, max(3.0, base_workload + random.uniform(0.2, 1.2)))
                study = min(11.0, max(4.0, base_study + random.uniform(1.0, 2.5)))
                sleep = min(8.5, max(4.0, base_sleep - random.uniform(0.2, 0.8)))
                screen = min(9.0, max(2.0, base_screen))
                activity = max(10, base_activity)
                social = max(0.5, base_social - random.uniform(0.5, 1.5))
                anxiety = min(10.0, max(3.0, 7.0 + random.uniform(-0.5, 1.5)))
                mood = max(1.0, min(10.0, 7.5 - anxiety * 0.4))
            elif primary_nature == "Time-pressure":
                workload = min(10.0, max(5.0, 7.5 + drift))
                study = min(11.0, max(4.0, 7.0))
                sleep = min(7.5, max(3.5, 5.0 - drift * 0.3))
                screen = min(11.0, max(5.0, 6.5 + random.uniform(0.5, 1.5)))
                activity = max(5, 20.0 - random.uniform(0, 10))
                social = max(0.5, 1.5 - random.uniform(0, 0.5))
                anxiety = min(10.0, max(4.0, 6.5 + workload * 0.3))
                mood = max(1.0, min(10.0, 6.5 - anxiety * 0.35))
            elif primary_nature == "Social":
                social = max(0.0, min(3.0, 1.5 - random.uniform(0, 0.8)))
                workload = min(10.0, max(2.0, base_workload))
                sleep = min(9.0, max(4.5, base_sleep))
                study = min(9.0, max(2.0, base_study))
                screen = min(12.0, max(5.0, base_screen + 1.5))
                activity = max(5, base_activity - 5)
                anxiety = min(10.0, max(2.0, 5.0 + (4 - social) * 0.6))
                mood = max(1.0, min(10.0, 5.0 + social * 0.6))
            else: # Mixed
                workload = min(10.0, max(3.0, base_workload + drift))
                sleep = min(8.5, max(3.5, base_sleep - drift * 0.4))
                study = min(10.0, max(3.0, base_study))
                screen = min(10.0, max(3.0, base_screen))
                activity = max(5, base_activity)
                social = max(0.5, base_social)
                anxiety = min(10.0, max(3.0, 5.5 + drift))
                mood = max(1.0, min(10.0, 6.0 - drift * 0.5))

            # Compute realistic ground truth stress severity (0-100)
            stress_score = (
                (10.0 - sleep) * 4.5 +
                workload * 4.0 +
                anxiety * 3.5 +
                (10.0 - mood) * 2.5 +
                (screen * 0.8) -
                (activity * 0.15) -
                (social * 1.2) +
                random.uniform(-3, 3)
            )
            stress_score = float(np.clip(stress_score, 10.0, 98.0))

            if stress_score < 35.0:
                severity_tier = "Low"
            elif stress_score < 60.0:
                severity_tier = "Moderate"
            elif stress_score < 80.0:
                severity_tier = "High"
            else:
                severity_tier = "Severe"

            journal_text = random.choice(journal_templates[primary_nature])

            top_factors = []
            if sleep < 6.0: top_factors.append("Sleep Deprivation")
            if workload > 6.5: top_factors.append("Heavy Academic Workload")
            if anxiety > 6.0: top_factors.append("Exam & Performance Anxiety")
            if screen > 7.0: top_factors.append("Excessive Screen Time")
            if activity < 20: top_factors.append("Low Physical Activity")
            if social < 2.0: top_factors.append("Social Isolation")
            if not top_factors: top_factors = ["General Workload Routine"]

            records.append({
                "student_id": student_id,
                "day": d,
                "sleep_hours": round(sleep, 2),
                "study_hours": round(study, 2),
                "screen_time_hours": round(screen, 2),
                "physical_activity_mins": round(activity, 1),
                "academic_workload_score": round(workload, 2),
                "social_activity_hours": round(social, 2),
                "anxiety_level": round(anxiety, 2),
                "mood_rating": round(mood, 2),
                "routine_consistency_score": round(random.uniform(3.0, 9.5), 2),
                "journal_entry": journal_text,
                "stress_score": round(stress_score, 2),
                "severity_tier": severity_tier,
                "stress_nature": primary_nature,
                "stress_trajectory": base_trend,
                "major_factors": json.dumps(top_factors)
            })

    df = pd.DataFrame(records)
    out_dir = os.path.join(os.path.dirname(__file__), "raw")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "student_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} student records across {num_students} students at {csv_path}")

if __name__ == "__main__":
    generate_student_dataset()
