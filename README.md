# 🧠 Student Stress Analyser

An intelligent **Student Stress Analysis and Recovery System** that combines **Machine Learning, Deep Learning, NLP, Explainable AI, and a web-based dashboard** to analyse student stress levels and provide personalized recovery recommendations.

## 📌 Project Overview

Student Stress Analyser is designed to identify and analyse stress among students using multiple factors such as academic pressure, lifestyle patterns, emotional state, and activity-related information.

The system combines **Machine Learning and Deep Learning models** to generate a comprehensive stress assessment and provides personalized recovery suggestions based on the predicted stress level.

## 🎯 Objectives

* Identify and classify student stress levels.
* Analyse academic, behavioural, lifestyle, and emotional factors.
* Use ML and Deep Learning for intelligent stress prediction.
* Analyse text-based emotional information using NLP.
* Provide explainable predictions using Explainable AI.
* Generate personalized recovery recommendations.
* Track stress and recovery progress through visual dashboards.

## 🚀 Key Features

### 📊 Stress Assessment

Collects student information and assessment responses to evaluate stress-related factors.

### 🤖 Machine Learning

Uses traditional ML techniques for stress prediction, preprocessing, feature engineering, and evaluation.

### 🧠 Deep Learning

Includes multiple deep learning components for analysing complex student behaviour and emotional patterns.

### 💬 NLP Analysis

Uses **DistilBERT** to analyse text-based emotional information.

### 🔗 Multimodal Fusion

Combines information from different sources to generate a more comprehensive stress assessment.

### 🔍 Explainable AI

Provides explanations for model predictions so that the important contributing factors can be understood.

### 📈 Visual Analytics

Displays stress factors, stress trends, activity patterns, emotional information, and recovery progress using interactive visualizations.

### 🌱 Recovery Recommendation

Provides personalized recovery suggestions based on the student's stress condition.

### 📅 Recovery Tracking

Tracks recovery activities and monitors progress over time.

## 🏗️ System Architecture

```text
                 Student Input
                      │
                      ▼
             ┌─────────────────┐
             │ Stress Assessment│
             └────────┬────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   Structured Data            Text Data
          │                       │
          ▼                       ▼
   Data Preprocessing       DistilBERT / NLP
          │                       │
          ▼                       ▼
     ML Models              Deep Learning
          │                       │
          └───────────┬───────────┘
                      ▼
              Multimodal Fusion
                      │
                      ▼
             Stress Prediction
                      │
             ┌────────┴────────┐
             ▼                 ▼
        Explainable AI    Stress Analysis
             │                 │
             └────────┬────────┘
                      ▼
           Recovery Recommendation
                      │
                      ▼
              Progress Tracking
                      │
                      ▼
               Visual Dashboard
```

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* FastAPI

### Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Joblib

### Deep Learning

* PyTorch
* LSTM
* DistilBERT
* Multimodal Fusion

### Data Processing

* Pandas
* NumPy
* Feature Engineering
* Data Preprocessing

### Explainable AI

* Explainable AI techniques for interpreting model predictions

### Visualization

* Python visualization libraries
* Stress trend analysis
* Activity analysis
* Recovery progress visualization

## 📁 Project Structure

```text
student-stress-project/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   │   ├── student.py
│   │   ├── assessment.py
│   │   ├── stress.py
│   │   ├── recovery.py
│   │   └── progress.py
│   └── services/
│       ├── stress_service.py
│       └── recovery_service.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── generate_dataset.py
│
├── ml/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train_ml.py
│   └── evaluate_ml.py
│
├── deep_learning/
│   ├── activity_lstm.py
│   ├── text_distilbert.py
│   ├── fusion_model.py
│   ├── train_dl.py
│   ├── evaluate_dl.py
│   └── explainable_ai.py
│
├── recovery/
│   ├── recommendation.py
│   ├── recovery_rules.py
│   └── recovery_tracker.py
│
├── visuals/
│   ├── stress_gauge.py
│   ├── stress_trend.py
│   ├── stress_factors.py
│   ├── activity_chart.py
│   ├── emotion_chart.py
│   ├── recovery_progress.py
│   └── recovery_effectiveness.py
│
├── frontend/
│   ├── index.html
│   ├── assessment.html
│   ├── dashboard.html
│   ├── result.html
│   ├── recovery.html
│   ├── progress.html
│   ├── css/
│   └── js/
│
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MRCUS-MOBIN/stress-analyser.git
```

### 2. Open the project

```bash
cd stress-analyser/student-stress-project
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Backend

From the `student-stress-project` directory:

```bash
python -m uvicorn backend.main:app --reload
```

The backend will run on:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🔄 Workflow

```text
Student
   ↓
Assessment & Data Collection
   ↓
Data Preprocessing
   ↓
Feature Engineering
   ↓
ML + Deep Learning Models
   ↓
Multimodal Fusion
   ↓
Stress Prediction
   ↓
Explainable AI
   ↓
Personalized Recovery
   ↓
Progress Tracking
   ↓
Visual Dashboard
```

## 💡 Innovation

The key innovation of this project is the combination of **traditional Machine Learning, Deep Learning, NLP, multimodal data fusion, Explainable AI, and personalized recovery tracking** into a single student stress analysis platform.

Instead of only predicting stress, the system attempts to provide an end-to-end workflow from **assessment → prediction → explanation → recovery → progress monitoring**.

## 🔮 Future Enhancements

* Real-time wearable sensor integration.
* Mobile application.
* Voice-based emotion analysis.
* Real-time stress monitoring.
* Advanced personalized recommendations.
* Cloud deployment.
* Real-time notification and alert system.

## 👩‍💻 Project

**Student Stress Analyser**

Developed as an intelligent web-based platform for student stress assessment, prediction, explainability, and recovery support.

## 📄 License

This project is developed for educational and project demonstration purposes.
