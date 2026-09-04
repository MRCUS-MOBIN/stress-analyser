from recovery.recommendation import PersonalizedRecoveryEngine
from recovery.recovery_tracker import RecoveryEffectivenessTracker

class RecoveryService:
    def __init__(self):
        self.engine = PersonalizedRecoveryEngine()
        self.tracker = RecoveryEffectivenessTracker()

    def get_personalized_recommendations(self, student_id, stress_profile):
        eff_profile = self.tracker.get_student_effectiveness_profile(student_id)
        return self.engine.generate_recommendations(stress_profile, eff_profile)

    def log_recovery_action(self, student_id, activity_id, activity_title, pre_stress, post_stress, duration_mins=20, notes=""):
        return self.tracker.log_recovery_action(
            student_id=student_id,
            activity_id=activity_id,
            activity_title=activity_title,
            pre_stress=pre_stress,
            post_stress=post_stress,
            duration_mins=duration_mins,
            notes=notes
        )

    def get_student_recovery_history(self, student_id):
        return self.tracker.get_student_recovery_logs(student_id)

    def get_student_effectiveness_profile(self, student_id):
        return self.tracker.get_student_effectiveness_profile(student_id)

recovery_service_instance = RecoveryService()
