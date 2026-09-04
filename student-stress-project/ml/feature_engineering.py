import pandas as pd
import numpy as np

def extract_engineered_features(df):
    df_feat = df.copy()
    
    # 1. Temporal & Activity Ratios
    # Sleep-to-Study Ratio (avoid divide by zero)
    df_feat["sleep_study_ratio"] = df_feat["sleep_hours"] / (df_feat["study_hours"] + 0.1)
    
    # Workload-to-Social Ratio
    df_feat["workload_social_ratio"] = df_feat["academic_workload_score"] / (df_feat["social_activity_hours"] + 0.1)
    
    # Screen-to-Sleep Ratio
    df_feat["screen_sleep_ratio"] = df_feat["screen_time_hours"] / (df_feat["sleep_hours"] + 0.1)
    
    # Rest vs Effort Index
    df_feat["rest_effort_index"] = (df_feat["sleep_hours"] + (df_feat["physical_activity_mins"] / 30.0)) - (df_feat["study_hours"] + df_feat["academic_workload_score"])

    # 2. Mood-Anxiety Gap
    df_feat["anxiety_mood_gap"] = df_feat["anxiety_level"] - df_feat["mood_rating"]

    # 3. Simple Text Sentiment Keyword Features
    high_stress_words = ["midterms", "anxious", "unprepared", "overwhelming", "exhausted", "insomnia", "isolated", "rejections"]
    def text_stress_score(text):
        if not isinstance(text, str): return 0.0
        text_lower = text.lower()
        score = sum(1.0 for w in high_stress_words if w in text_lower)
        return min(5.0, score)

    if "journal_entry" in df_feat.columns:
        df_feat["text_keyword_stress"] = df_feat["journal_entry"].apply(text_stress_score)
    else:
        df_feat["text_keyword_stress"] = 0.0

    return df_feat

if __name__ == "__main__":
    from ml.preprocessing import load_raw_data, clean_data
    df_raw = load_raw_data()
    df_clean = clean_data(df_raw)
    df_eng = extract_engineered_features(df_clean)
    print("Engineered features extracted successfully! Columns:", df_eng.columns.tolist()[-6:])
