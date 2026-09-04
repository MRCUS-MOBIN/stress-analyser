const API_BASE_URL = "http://localhost:8000/api";

const ApiClient = {
  async registerStudent(studentData) {
    try {
      const res = await fetch(`${API_BASE_URL}/student/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(studentData)
      });
      return await res.json();
    } catch (e) {
      console.warn("API offline fallback for registerStudent");
      return { message: "Student logged in (Offline)", student: { student_id: "STU_001", name: studentData.name } };
    }
  },

  async submitAssessment(assessmentData) {
    try {
      const res = await fetch(`${API_BASE_URL}/assessment/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(assessmentData)
      });
      return await res.json();
    } catch (e) {
      console.warn("API offline fallback for submitAssessment");
      return {
        message: "Assessment analyzed (Offline Preview)",
        assessment_id: "ASM_MOCK_123",
        stress_profile: {
          severity_score: 74.5,
          severity_tier: "High",
          stress_nature: "Academic",
          stress_trajectory: "Increasing",
          major_factors: [
            { factor: "Academic Workload & Deadlines", percentage: 38.5, impact_score: 28.0 },
            { factor: "Sleep Deprivation & Disrupted Sleep", percentage: 32.0, impact_score: 23.3 },
            { factor: "Exam & Performance Pressure", percentage: 18.5, impact_score: 13.5 },
            { factor: "Excessive Screen Time", percentage: 11.0, impact_score: 8.0 }
          ],
          xai_explanation: "The primary driver of stress is Academic Workload & Deadlines (38.5% contribution), followed by Sleep Deprivation (32.0%).",
          model_comparisons: {
            "Multimodal_Fusion_DL": 74.5,
            "Random_Forest_Baseline": 72.8,
            "Gradient_Boosting_Baseline": 75.2
          }
        }
      };
    }
  },

  async getLatestStressProfile(studentId = "STU_001") {
    try {
      const res = await fetch(`${API_BASE_URL}/stress/profile/${studentId}`);
      return await res.json();
    } catch (e) {
      console.warn("API offline fallback for getLatestStressProfile");
      return {
        student_id: studentId,
        severity_score: 74.5,
        severity_tier: "High",
        stress_nature: "Academic",
        stress_trajectory: "Increasing",
        major_factors: [
          { factor: "Academic Workload & Deadlines", percentage: 38.5, impact_score: 28.0 },
          { factor: "Sleep Deprivation & Disrupted Sleep", percentage: 32.0, impact_score: 23.3 },
          { factor: "Exam & Performance Pressure", percentage: 18.5, impact_score: 13.5 },
          { factor: "Excessive Screen Time", percentage: 11.0, impact_score: 8.0 }
        ],
        xai_explanation: "The primary driver of stress is Academic Workload & Deadlines (38.5% contribution), followed by Sleep Deprivation (32.0%).",
        model_comparisons: {
          "Multimodal_Fusion_DL": 74.5,
          "Random_Forest_Baseline": 72.8,
          "Gradient_Boosting_Baseline": 75.2
        }
      };
    }
  },

  async getRecoveryRecommendations(studentId = "STU_001") {
    try {
      const res = await fetch(`${API_BASE_URL}/recovery/recommendations/${studentId}`);
      return await res.json();
    } catch (e) {
      console.warn("API offline fallback for getRecoveryRecommendations");
      return {
        stress_nature: "Academic",
        severity_tier: "High",
        total_recommended: 4,
        recommendations: [
          {
            id: "rec_pomodoro",
            title: "Structured Pomodoro Study & Break Routine",
            category: "Workload Management",
            description: "Study in focused 25-minute bursts followed by 5-minute restorative breaks to reduce cognitive fatigue.",
            estimated_time_mins: 30,
            personalized_effectiveness_score: 88.0,
            is_personalized_priority: true
          },
          {
            id: "rec_digital_detox",
            title: "90-Min Pre-Bedtime Digital Screen Wind-Down",
            category: "Sleep Hygiene",
            description: "Turn off high-blue-light screens 90 minutes before bedtime to activate melatonin synthesis.",
            estimated_time_mins: 90,
            personalized_effectiveness_score: 94.5,
            is_personalized_priority: true
          },
          {
            id: "rec_box_breathing",
            title: "4-7-8 Deep Diaphragmatic Box Breathing",
            category: "Anxiety Reduction",
            description: "Regulate nervous system arousal before study sessions or mock presentations.",
            estimated_time_mins: 10,
            personalized_effectiveness_score: 90.0,
            is_personalized_priority: false
          },
          {
            id: "rec_cardio_exercise",
            title: "30-Min Aerobic Physical Activity",
            category: "Physical Wellness",
            description: "Engage in moderate jogging, swimming, cycling, or gym exercise to release endorphins.",
            estimated_time_mins: 30,
            personalized_effectiveness_score: 86.0,
            is_personalized_priority: false
          }
        ]
      };
    }
  },

  async logRecoveryAction(logData) {
    try {
      const res = await fetch(`${API_BASE_URL}/recovery/log`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(logData)
      });
      return await res.json();
    } catch (e) {
      console.warn("API offline fallback for logRecoveryAction");
      return { message: "Recovery action logged (Offline)", log_entry: logData };
    }
  },

  async getDashboardData(studentId = "STU_001") {
    try {
      const res = await fetch(`${API_BASE_URL}/progress/dashboard/${studentId}`);
      return await res.json();
    } catch (e) {
      console.warn("API offline fallback for getDashboardData");
      return null;
    }
  }
};