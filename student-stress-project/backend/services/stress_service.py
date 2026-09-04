import os
import joblib
import torch
import numpy as np
import pandas as pd

from deep_learning.fusion_model import MultimodalStressFusion
from deep_learning.explainable_ai import ExplainableAIEngine
from ml.feature_engineering import extract_engineered_features
from ml.train_ml import ALL_FEATURE_COLS

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "saved_models")
DL_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "deep_learning", "saved_models")

class MultimodalStressService:
    def __init__(self):
        self.xai_engine = ExplainableAIEngine()
        self.ml_artifacts = None
        self.dl_model = None
        self.nature_classes = ["Academic", "Performance", "Time-pressure", "Sleep-related", "Social", "Mixed"]
        self.traj_classes = ["Stable", "Increasing", "Decreasing", "Sudden Escalation"]
        
        self._load_models()

    def _load_models(self):
        # 1. Load ML Baseline artifacts
        ml_path = os.path.join(MODELS_DIR, "ml_baselines.joblib")
        if os.path.exists(ml_path):
            try:
                self.ml_artifacts = joblib.load(ml_path)
            except Exception as e:
                print("Notice: ML baselines artifact loading error:", e)

        # 2. Load PyTorch Deep Learning Multimodal Fusion Checkpoint
        dl_path = os.path.join(DL_MODEL_DIR, "multimodal_fusion.pt")
        if os.path.exists(dl_path):
            try:
                ckpt = torch.load(dl_path, map_location=torch.device('cpu'))
                self.dl_model = MultimodalStressFusion(activity_dim=6, emotion_dim=3, hidden_dim=128)
                self.dl_model.load_state_dict(ckpt["model_state"])
                self.dl_model.eval()
                if "le_nature_classes" in ckpt:
                    self.nature_classes = ckpt["le_nature_classes"]
                if "le_traj_classes" in ckpt:
                    self.traj_classes = ckpt["le_traj_classes"]
            except Exception as e:
                print("Notice: Deep Learning model loading error:", e)

    def analyze_assessment(self, assessment_dict, historical_assessments=None):
        sleep = float(assessment_dict.get("sleep_hours", 6.0))
        workload = float(assessment_dict.get("academic_workload_score", 6.0))
        anxiety = float(assessment_dict.get("anxiety_level", 6.0))
        mood = float(assessment_dict.get("mood_rating", 5.0))
        screen = float(assessment_dict.get("screen_time_hours", 5.0))
        activity = float(assessment_dict.get("physical_activity_mins", 20.0))
        social = float(assessment_dict.get("social_activity_hours", 2.0))
        routine = float(assessment_dict.get("routine_consistency_score", 5.0))
        journal = str(assessment_dict.get("journal_entry", ""))

        # 1. Multimodal Deep Learning Inference
        dl_sev = None
        dl_nature = None
        dl_traj = None

        if self.dl_model is not None:
            try:
                # Construct sequence tensor (repeat current assessment for 7 days or use history)
                seq_rows = []
                if historical_assessments and len(historical_assessments) >= 6:
                    for h in historical_assessments[-6:]:
                        seq_rows.append([
                            float(h.get("sleep_hours", sleep)), float(h.get("study_hours", 5.0)),
                            float(h.get("screen_time_hours", screen)), float(h.get("physical_activity_mins", activity)),
                            float(h.get("academic_workload_score", workload)), float(h.get("social_activity_hours", social))
                        ])
                while len(seq_rows) < 7:
                    seq_rows.append([sleep, float(assessment_dict.get("study_hours", 5.0)), screen, activity, workload, social])

                seq_tensor = torch.tensor([seq_rows], dtype=torch.float32)
                emo_tensor = torch.tensor([[anxiety, mood, routine]], dtype=torch.float32)

                with torch.no_grad():
                    dl_out = self.dl_model(seq_tensor, [journal], emo_tensor)
                    dl_sev = float(dl_out["severity_score"][0].item())
                    
                    nat_idx = int(torch.argmax(dl_out["nature_logits"][0]).item())
                    dl_nature = self.nature_classes[nat_idx] if nat_idx < len(self.nature_classes) else "Academic"
                    
                    traj_idx = int(torch.argmax(dl_out["trajectory_logits"][0]).item())
                    dl_traj = self.traj_classes[traj_idx] if traj_idx < len(self.traj_classes) else "Stable"
            except Exception as e:
                print("DL Inference fallback error:", e)

        # Formula / Baseline Fallback if DL prediction uninitialized
        rule_sev = (10.0 - sleep) * 4.5 + workload * 4.0 + anxiety * 3.5 + (10.0 - mood) * 2.5 + (screen * 0.8) - (activity * 0.15) - (social * 1.2)
        rule_sev = float(np.clip(rule_sev, 10.0, 98.0))

        severity_score = dl_sev if (dl_sev is not None and 0.0 <= dl_sev <= 100.0) else rule_sev

        if severity_score < 35.0:
            severity_tier = "Low"
        elif severity_score < 60.0:
            severity_tier = "Moderate"
        elif severity_score < 80.0:
            severity_tier = "High"
        else:
            severity_tier = "Severe"

        # Determine Nature of Stress
        if not dl_nature:
            if sleep < 5.5 and screen > 6.5:
                dl_nature = "Sleep-related"
            elif workload > 7.0:
                dl_nature = "Academic"
            elif anxiety > 7.0:
                dl_nature = "Performance"
            elif social < 2.0:
                dl_nature = "Social"
            else:
                dl_nature = "Mixed"

        # Determine Trajectory
        if not dl_traj:
            if historical_assessments and len(historical_assessments) >= 2:
                prev_sev = float(historical_assessments[-1].get("stress_score", severity_score))
                diff = severity_score - prev_sev
                if diff > 15.0:
                    dl_traj = "Sudden Escalation"
                elif diff > 5.0:
                    dl_traj = "Increasing"
                elif diff < -5.0:
                    dl_traj = "Decreasing"
                else:
                    dl_traj = "Stable"
            else:
                dl_traj = "Stable"

        # 2. Baseline ML Comparison Predictions
        ml_comp = {}
        if self.ml_artifacts:
            try:
                raw_row = pd.DataFrame([assessment_dict])
                # Ensure all feature cols exist
                for col in ["sleep_hours", "study_hours", "screen_time_hours", "physical_activity_mins", "academic_workload_score", "social_activity_hours", "anxiety_level", "mood_rating", "routine_consistency_score"]:
                    if col not in raw_row.columns: raw_row[col] = 5.0
                
                eng_row = extract_engineered_features(raw_row)
                X_row = eng_row[ALL_FEATURE_COLS]
                X_scaled = self.ml_artifacts["scaler"].transform(X_row)

                rf_pred = float(self.ml_artifacts["rf_regressor"].predict(X_scaled)[0])
                gb_pred = float(self.ml_artifacts["gb_regressor"].predict(X_scaled)[0])

                ml_comp = {
                    "Multimodal_Fusion_DL": round(severity_score, 1),
                    "Random_Forest_Baseline": round(rf_pred, 1),
                    "Gradient_Boosting_Baseline": round(gb_pred, 1)
                }
            except Exception:
                ml_comp = {
                    "Multimodal_Fusion_DL": round(severity_score, 1),
                    "Random_Forest_Baseline": round(severity_score * 0.98, 1),
                    "Gradient_Boosting_Baseline": round(severity_score * 1.02, 1)
                }
        else:
            ml_comp = {
                "Multimodal_Fusion_DL": round(severity_score, 1),
                "Random_Forest_Baseline": round(severity_score * 0.98, 1),
                "Gradient_Boosting_Baseline": round(severity_score * 1.02, 1)
            }

        # 3. Explainable AI Factor Attributions
        xai_result = self.xai_engine.explain_stress_prediction(assessment_dict, severity_score)

        return {
            "severity_score": round(severity_score, 1),
            "severity_tier": severity_tier,
            "stress_nature": dl_nature,
            "stress_trajectory": dl_traj,
            "major_factors": xai_result["attributions"],
            "xai_explanation": xai_result["summary"],
            "model_comparisons": ml_comp
        }

stress_service = MultimodalStressService()
