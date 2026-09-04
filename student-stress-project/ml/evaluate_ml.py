import os
import joblib
import json
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, f1_score, precision_score, recall_score
from ml.preprocessing import load_raw_data, clean_data, MODELS_DIR
from ml.feature_engineering import extract_engineered_features
from ml.train_ml import ALL_FEATURE_COLS

def evaluate_baseline_models():
    model_path = os.path.join(MODELS_DIR, "ml_baselines.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError("ML Baselines model artifact not found. Please run ml/train_ml.py first.")

    artifacts = joblib.load(model_path)
    scaler = artifacts["scaler"]
    le_tier = artifacts["le_tier"]
    rf_reg = artifacts["rf_regressor"]
    gb_reg = artifacts["gb_regressor"]
    ridge_reg = artifacts["ridge_regressor"]
    rf_cls = artifacts["rf_classifier"]
    gb_cls = artifacts["gb_classifier"]
    log_reg = artifacts["logistic_regression"]

    df_raw = load_raw_data()
    df = extract_engineered_features(clean_data(df_raw))

    X = df[ALL_FEATURE_COLS]
    y_score = df["stress_score"]
    y_tier = le_tier.transform(df["severity_tier"])

    X_scaled = scaler.transform(X)

    # Evaluate Regression
    results = {}
    for name, reg in [("Ridge Regression", ridge_reg), ("Random Forest Regressor", rf_reg), ("Gradient Boosting Regressor", gb_reg)]:
        preds = reg.predict(X_scaled)
        results[name] = {
            "RMSE": round(float(np.sqrt(mean_squared_error(y_score, preds))), 4),
            "MAE": round(float(mean_absolute_error(y_score, preds)), 4),
            "R2_Score": round(float(r2_score(y_score, preds)), 4)
        }

    # Evaluate Classification
    for name, cls in [("Logistic Regression", log_reg), ("Random Forest Classifier", rf_cls), ("Gradient Boosting Classifier", gb_cls)]:
        preds = cls.predict(X_scaled)
        results[name] = {
            "Accuracy": round(float(accuracy_score(y_tier, preds)), 4),
            "F1_Score": round(float(f1_score(y_tier, preds, average="weighted")), 4),
            "Precision": round(float(precision_score(y_tier, preds, average="weighted")), 4),
            "Recall": round(float(recall_score(y_tier, preds, average="weighted")), 4)
        }

    out_path = os.path.join(MODELS_DIR, "ml_eval_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print("=== Baseline ML Models Evaluation Results ===")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    evaluate_baseline_models()
