import os
import json
from datetime import datetime

RECOVERY_LOGS_FILE = os.path.join(os.path.dirname(__file__), "recovery_history.json")

class RecoveryEffectivenessTracker:
    """
    Recovery Effectiveness Mechanism.
    Records student recovery actions, compares stress level before & after intervention,
    and updates individual student Personalized Recovery Effectiveness Profiles.
    """
    def __init__(self, filepath=RECOVERY_LOGS_FILE):
        self.filepath = filepath
        self._ensure_storage()

    def _ensure_storage(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump({"logs": [], "student_profiles": {}}, f, indent=2)

    def _load_data(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except Exception:
            return {"logs": [], "student_profiles": {}}

    def _save_data(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def log_recovery_action(self, student_id, activity_id, activity_title, pre_stress, post_stress, duration_mins=20, notes=""):
        data = self._load_data()
        
        stress_reduction = round(max(0.0, float(pre_stress) - float(post_stress)), 2)
        percentage_reduction = round((stress_reduction / (float(pre_stress) + 1e-5)) * 100.0, 1)

        entry = {
            "log_id": f"REC_{datetime.now().strftime('%Y%m%d%H%M%S')}_{student_id}",
            "student_id": student_id,
            "activity_id": activity_id,
            "activity_title": activity_title,
            "timestamp": datetime.now().isoformat(),
            "pre_stress_score": float(pre_stress),
            "post_stress_score": float(post_stress),
            "stress_reduction": stress_reduction,
            "percentage_reduction": percentage_reduction,
            "duration_mins": duration_mins,
            "notes": notes
        }

        data["logs"].append(entry)

        # Update student's personalized recovery profile
        student_id_str = str(student_id)
        if student_id_str not in data["student_profiles"]:
            data["student_profiles"][student_id_str] = {}

        st_profile = data["student_profiles"][student_id_str]
        
        if activity_id not in st_profile:
            st_profile[activity_id] = {
                "activity_title": activity_title,
                "times_completed": 1,
                "total_reduction": stress_reduction,
                "average_reduction": stress_reduction,
                "average_percentage_improvement": percentage_reduction,
                "effectiveness_score": min(100.0, percentage_reduction * 2.5 + 40.0)
            }
        else:
            prev = st_profile[activity_id]
            n = prev["times_completed"] + 1
            tot_red = prev["total_reduction"] + stress_reduction
            avg_red = tot_red / n
            avg_pct = (prev["average_percentage_improvement"] * (n - 1) + percentage_reduction) / n
            
            st_profile[activity_id] = {
                "activity_title": activity_title,
                "times_completed": n,
                "total_reduction": round(tot_red, 2),
                "average_reduction": round(avg_red, 2),
                "average_percentage_improvement": round(avg_pct, 1),
                "effectiveness_score": round(min(100.0, avg_pct * 2.5 + 40.0), 1)
            }

        self._save_data(data)
        return entry

    def get_student_effectiveness_profile(self, student_id):
        data = self._load_data()
        student_id_str = str(student_id)
        st_profile = data["student_profiles"].get(student_id_str, {})
        
        # Return map { activity_id: effectiveness_score }
        return {act_id: info["effectiveness_score"] for act_id, info in st_profile.items()}

    def get_student_recovery_logs(self, student_id):
        data = self._load_data()
        return [l for l in data["logs"] if str(l["student_id"]) == str(student_id)]

if __name__ == "__main__":
    tracker = RecoveryEffectivenessTracker()
    entry = tracker.log_recovery_action(
        student_id="STU_001",
        activity_id="rec_box_breathing",
        activity_title="4-7-8 Deep Diaphragmatic Box Breathing",
        pre_stress=78.5,
        post_stress=52.0,
        duration_mins=10
    )
    print("Logged Recovery Action:", entry["log_id"])
    print("Updated Effectiveness Profile:", tracker.get_student_effectiveness_profile("STU_001"))
