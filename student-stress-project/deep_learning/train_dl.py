import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from deep_learning.fusion_model import MultimodalStressFusion
from ml.preprocessing import load_raw_data, clean_data, MODELS_DIR

DL_MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")

def build_sequential_dataset(df):
    """
    Groups data by student_id and builds 7-day sequences for ActivityLSTM,
    along with text entries and emotion vectors.
    """
    students = df["student_id"].unique()
    
    seq_list = []
    text_list = []
    emotion_list = []
    severity_list = []
    nature_list = []
    trajectory_list = []
    
    le_nature = LabelEncoder()
    le_nature.fit(["Academic", "Performance", "Time-pressure", "Sleep-related", "Social", "Mixed"])
    
    le_traj = LabelEncoder()
    le_traj.fit(["Stable", "Increasing", "Decreasing", "Sudden Escalation"])
    
    activity_cols = ["sleep_hours", "study_hours", "screen_time_hours", "physical_activity_mins", "academic_workload_score", "social_activity_hours"]

    for sid in students:
        sdf = df[df["student_id"] == sid].sort_values("day")
        if len(sdf) < 7: continue

        seq_acts = sdf[activity_cols].values # (7, 6)
        
        # Take target from final day in sequence
        last_row = sdf.iloc[-1]
        
        seq_list.append(seq_acts)
        text_list.append(str(last_row["journal_entry"]))
        emotion_list.append([last_row["anxiety_level"], last_row["mood_rating"], last_row["routine_consistency_score"]])
        severity_list.append(last_row["stress_score"])
        nature_list.append(le_nature.transform([last_row["stress_nature"]])[0])
        trajectory_list.append(le_traj.transform([last_row["stress_trajectory"]])[0])

    X_seq = torch.tensor(np.array(seq_list), dtype=torch.float32)
    X_emo = torch.tensor(np.array(emotion_list), dtype=torch.float32)
    Y_sev = torch.tensor(np.array(severity_list), dtype=torch.float32)
    Y_nat = torch.tensor(np.array(nature_list), dtype=torch.long)
    Y_traj = torch.tensor(np.array(trajectory_list), dtype=torch.long)

    return X_seq, text_list, X_emo, Y_sev, Y_nat, Y_traj, le_nature, le_traj

def train_multimodal_dl():
    os.makedirs(DL_MODEL_DIR, exist_ok=True)
    df_raw = load_raw_data()
    df = clean_data(df_raw)

    X_seq, texts, X_emo, Y_sev, Y_nat, Y_traj, le_nat, le_traj = build_sequential_dataset(df)

    # Normalize Y_sev (0-100) to 0.0-1.0 for smooth training
    Y_sev_norm = Y_sev / 100.0

    model = MultimodalStressFusion(activity_dim=6, emotion_dim=3, hidden_dim=128)
    optimizer = optim.AdamW(model.parameters(), lr=0.005, weight_decay=1e-4)

    criterion_sev = nn.MSELoss()
    criterion_nat = nn.CrossEntropyLoss()
    criterion_traj = nn.CrossEntropyLoss()

    epochs = 120
    print(f"Training Multimodal Deep Learning Fusion Model on {len(X_seq)} student sequences for {epochs} epochs...")

    model.train()
    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()
        out = model(X_seq, texts, X_emo)

        loss_sev = criterion_sev(out["severity_score"] / 100.0, Y_sev_norm)
        loss_nat = criterion_nat(out["nature_logits"], Y_nat)
        loss_traj = criterion_traj(out["trajectory_logits"], Y_traj)

        total_loss = 5.0 * loss_sev + 1.0 * loss_nat + 1.0 * loss_traj

        total_loss.backward()
        optimizer.step()

        if epoch % 20 == 0 or epoch == 1:
            print(f"Epoch [{epoch:03d}/{epochs}] - Loss: {total_loss.item():.4f} (Sev MSE: {loss_sev.item():.4f}, Nat CE: {loss_nat.item():.3f}, Traj CE: {loss_traj.item():.3f})")

    # Save model weights & label encoders
    save_path = os.path.join(DL_MODEL_DIR, "multimodal_fusion.pt")
    torch.save({
        "model_state": model.state_dict(),
        "le_nature_classes": le_nat.classes_.tolist(),
        "le_traj_classes": le_traj.classes_.tolist()
    }, save_path)
    print(f"Multimodal Fusion DL model successfully saved to {save_path}")

if __name__ == "__main__":
    train_multimodal_dl()
