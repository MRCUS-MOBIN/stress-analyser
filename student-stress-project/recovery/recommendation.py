import copy
from recovery.recovery_rules import RECOVERY_KNOWLEDGE_BASE

class PersonalizedRecoveryEngine:
    """
    Personalized Recovery Engine.
    Generates targeted recovery recommendations tailored to the student's detected stress pattern,
    and dynamically re-ranks activities based on individual student effectiveness history.
    """
    def __init__(self):
        self.knowledge_base = RECOVERY_KNOWLEDGE_BASE

    def generate_recommendations(self, stress_profile, student_effectiveness_profile=None):
        """
        stress_profile dict:
          - stress_nature: e.g. "Academic", "Sleep-related"
          - severity_score: e.g. 74.5
          - severity_tier: e.g. "High"
          - major_factors: list of factor strings
          - trajectory: e.g. "Increasing"
          
        student_effectiveness_profile dict: { activity_id: efficiency_score (e.g. 0-100) }
        """
        nature = stress_profile.get("stress_nature", "Mixed")
        severity = stress_profile.get("severity_score", 50.0)
        factors = stress_profile.get("major_factors", [])

        # 1. Primary candidate set from primary stress nature
        candidates = copy.deepcopy(self.knowledge_base.get(nature, self.knowledge_base["Mixed"]))
        
        # 2. Secondary candidate set from secondary triggers
        secondary_natures = []
        if "Sleep Deprivation" in str(factors) and nature != "Sleep-related":
            secondary_natures.append("Sleep-related")
        if "Academic Workload" in str(factors) and nature != "Academic":
            secondary_natures.append("Academic")
        if "Exam" in str(factors) and nature != "Performance":
            secondary_natures.append("Performance")
        if "Social" in str(factors) and nature != "Social":
            secondary_natures.append("Social")

        for sec in secondary_natures:
            sec_items = self.knowledge_base.get(sec, [])
            for item in sec_items:
                if not any(c["id"] == item["id"] for c in candidates):
                    candidates.append(copy.deepcopy(item))

        # Always add physical exercise/journaling from Mixed if high severity
        if severity >= 65.0:
            for item in self.knowledge_base["Mixed"]:
                if not any(c["id"] == item["id"] for c in candidates):
                    candidates.append(copy.deepcopy(item))

        # 3. Dynamic Re-ranking using Personalized Recovery Effectiveness Profile
        eff_map = student_effectiveness_profile or {}

        for rec in candidates:
            rec_id = rec["id"]
            base_score = rec.get("base_effectiveness", 8.0)
            
            # Personal historical effectiveness weight
            if rec_id in eff_map:
                user_eff = eff_map[rec_id] # e.g. 92.5
                combined_score = (base_score * 0.4) + (user_eff / 10.0 * 0.6)
                rec["personalized_effectiveness_score"] = round(combined_score * 10, 1)
                rec["is_personalized_priority"] = True
            else:
                rec["personalized_effectiveness_score"] = round(base_score * 10, 1)
                rec["is_personalized_priority"] = False

        # Sort descending by personalized effectiveness score
        candidates.sort(key=lambda x: x["personalized_effectiveness_score"], reverse=True)

        return {
            "stress_nature": nature,
            "severity_tier": stress_profile.get("severity_tier", "Moderate"),
            "total_recommended": len(candidates),
            "recommendations": candidates[:4] # Top 4 personalized interventions
        }

if __name__ == "__main__":
    engine = PersonalizedRecoveryEngine()
    dummy_profile = {
        "stress_nature": "Academic",
        "severity_score": 75.0,
        "severity_tier": "High",
        "major_factors": ["Sleep Deprivation", "Heavy Academic Workload"],
        "trajectory": "Increasing"
    }
    dummy_eff = {"rec_digital_detox": 95.0, "rec_pomodoro": 88.0}
    recs = engine.generate_recommendations(dummy_profile, dummy_eff)
    print("Personalized Recommendations:", [r["title"] for r in recs["recommendations"]])
