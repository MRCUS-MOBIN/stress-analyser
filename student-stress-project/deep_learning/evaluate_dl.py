import os
import torch
import json
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, f1_score
from deep_learning.fusion_model import MultimodalStressFusion
from deep_learning.train_dl import build_sequential_dataset, DL_MODEL_DIR
from ml.preprocessing import load_raw_data, clean_data

def evaluate_multimodal_dl():
    ckpt_path = os.path.join(DL_MODEL_DIR, "multimodal_fusion.pt")
    if not os.path.exists(ckpt_path):
        raise FileNotFoundError(f"Deep learning checkpoint not found at {ckpt_path}. Run train_dl.py first.")

    checkpoint = torch.load(ckpt_path)
    model = MultimodalStressFusion(activity_dim=6, emotion_dim=3, hidden_dim=128)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    df_raw = load_raw_data()
    df = clean_data(df_raw)
    X_seq, texts, X_emo, Y_sev, Y_nat, Y_traj, le_nat, le_traj = build_sequential_dataset(df)

    with torch.no_grad():
        out = model(X_seq, texts, X_emo)
        pred_sev = out["severity_score"].numpy()
        pred_nat = torch.argmax(out["nature_logits"], dim=1).numpy()
        pred_traj = torch.argmax(out["trajectory_logits"], dim=1).numpy()

    true_sev = Y_sev.numpy()
    true_nat = Y_nat.numpy()
    true_traj = Y_traj.numpy()

    eval_results = {
        "Multimodal_Fusion_Severity_Regression": {
            "RMSE": round(float(np.sqrt(mean_squared_error(true_sev, pred_sev))), 4),
            "MAE": round(float(mean_absolute_error(true_sev, pred_sev)), 4),
            "R2_Score": round(float(r2_score(true_sev, pred_sev)), 4)
        },
        "Multimodal_Fusion_Stress_Nature_Classification": {
            "Accuracy": round(float(accuracy_score(true_nat, pred_nat)), 4),
            "F1_Score": round(float(f1_score(true_nat, pred_nat, average="weighted")), 4)
        },
        "Multimodal_Fusion_Stress_Trajectory_Classification": {
            "Accuracy": round(float(accuracy_score(true_traj, pred_traj)), 4),
            "F1_Score": round(float(f1_score(true_traj, pred_traj, average="weighted")), 4)
        }
    }

    out_json = os.path.join(DL_MODEL_DIR, "dl_eval_results.json")
    with open(out_json, "w") as f:
        json.dump(eval_results, f, indent=2)

    print("=== Multimodal Deep Learning Model Evaluation Results ===")
    print(json.dumps(eval_results, indent=2))
    return eval_results

if __name__ == "__main__":
    evaluate_multimodal_dl()
