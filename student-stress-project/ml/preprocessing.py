import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

DATA_RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "student_data.csv")
DATA_PROCESSED_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "processed_data.csv")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "saved_models")

FEATURE_COLS = [
    "sleep_hours", "study_hours", "screen_time_hours",
    "physical_activity_mins", "academic_workload_score",
    "social_activity_hours", "anxiety_level", "mood_rating",
    "routine_consistency_score"
]

NATURE_CLASSES = ["Academic", "Performance", "Time-pressure", "Sleep-related", "Social", "Mixed"]
TRAJECTORY_CLASSES = ["Stable", "Increasing", "Decreasing", "Sudden Escalation"]

def load_raw_data(path=DATA_RAW_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Raw data file not found at {path}. Run data generator first.")
    df = pd.read_csv(path)
    return df

def clean_data(df):
    df = df.copy()
    # Impute numeric missing values with median
    for col in FEATURE_COLS:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    
    # Fill text missing values
    if "journal_entry" in df.columns:
        df["journal_entry"] = df["journal_entry"].fillna("Feeling normal today.")
    
    return df

def preprocess_and_save(raw_path=DATA_RAW_PATH, processed_path=DATA_PROCESSED_PATH):
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)

    df = load_raw_data(raw_path)
    df = clean_data(df)

    # Fit Scaler on numeric features
    scaler = StandardScaler()
    scaled_feats = scaler.fit_transform(df[FEATURE_COLS])
    
    scaled_df = pd.DataFrame(scaled_feats, columns=[f"{c}_scaled" for c in FEATURE_COLS])
    df = pd.concat([df, scaled_df], axis=1)

    # Save preprocessing objects
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.joblib"))

    df.to_csv(processed_path, index=False)
    print(f"Processed data saved to {processed_path} with shape {df.shape}")
    return df

if __name__ == "__main__":
    preprocess_and_save()
