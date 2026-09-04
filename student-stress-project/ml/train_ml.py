import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.preprocessing import LabelEncoder, StandardScaler
from ml.preprocessing import preprocess_and_save, FEATURE_COLS, MODELS_DIR
from ml.feature_engineering import extract_engineered_features

ENGINEERED_COLS = [
    "sleep_study_ratio", "workload_social_ratio", "screen_sleep_ratio",
    "rest_effort_index", "anxiety_mood_gap", "text_keyword_stress"
]

ALL_FEATURE_COLS = FEATURE_COLS + ENGINEERED_COLS

def train_baseline_models():
    # 1. Preprocess & Feature Engineer
    df_proc = preprocess_and_save()
    df = extract_engineered_features(df_proc)

    X = df[ALL_FEATURE_COLS]
    y_score = df["stress_score"]
    y_tier = df["severity_tier"]
    y_nature = df["stress_nature"]

    # Encode categorical targets
    le_tier = LabelEncoder()
    y_tier_enc = le_tier.fit_transform(y_tier)
    
    le_nature = LabelEncoder()
    y_nature_enc = le_nature.fit_transform(y_nature)

    # Train/Test Split
    X_train, X_test, y_s_train, y_s_test, y_t_train, y_t_test = train_test_split(
        X, y_score, y_tier_enc, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"Training Baseline ML Models on {len(X_train)} samples...")

    # --- 1. Stress Score Regressors ---
    rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_reg.fit(X_train_scaled, y_s_train)

    gb_reg = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_reg.fit(X_train_scaled, y_s_train)

    ridge_reg = Ridge(alpha=1.0)
    ridge_reg.fit(X_train_scaled, y_s_train)

    # --- 2. Stress Tier Classifiers ---
    rf_cls = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_cls.fit(X_train_scaled, y_t_train)

    gb_cls = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb_cls.fit(X_train_scaled, y_t_train)

    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    log_reg.fit(X_train_scaled, y_t_train)

    # --- 3. Save Artifacts ---
    artifacts = {
        "scaler": scaler,
        "le_tier": le_tier,
        "le_nature": le_nature,
        "rf_regressor": rf_reg,
        "gb_regressor": gb_reg,
        "ridge_regressor": ridge_reg,
        "rf_classifier": rf_cls,
        "gb_classifier": gb_cls,
        "logistic_regression": log_reg,
        "feature_names": ALL_FEATURE_COLS
    }

    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(artifacts, os.path.join(MODELS_DIR, "ml_baselines.joblib"))
    print("Baseline ML models successfully trained and saved to ml/saved_models/ml_baselines.joblib")

if __name__ == "__main__":
    train_baseline_models()
