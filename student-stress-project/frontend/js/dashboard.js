document.addEventListener("DOMContentLoaded", async () => {
  const dashData = await ApiClient.getDashboardData("STU_001");
  renderFullDashboard(dashData);
});

function renderFullDashboard(data) {
  // 1. Gauge Score
  const gaugeElem = document.getElementById("dashGaugeScore");
  if (gaugeElem) gaugeElem.textContent = parseFloat(data?.latest_score || 74.5).toFixed(1);

  // 2. Trajectory Line Chart
  const ctxTrend = document.getElementById("dashTrendChart")?.getContext("2d");
  if (ctxTrend) {
    const trendConfig = data?.trend_chart || {
      labels: ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6"],
      datasets: [
        { label: "Stress Trajectory", data: [52.0, 58.0, 64.0, 61.0, 71.0, 74.5], borderColor: "#6366f1", backgroundColor: "rgba(99, 102, 241, 0.15)", fill: true, tension: 0.4 }
      ]
    };
    new Chart(ctxTrend, { type: "line", data: trendConfig, options: { responsive: true, maintainAspectRatio: false } });
  }

  // 3. XAI Factors Bar Chart
  const ctxFactors = document.getElementById("dashFactorsChart")?.getContext("2d");
  if (ctxFactors) {
    const factorsConfig = data?.factors_chart || {
      labels: ["Workload", "Sleep Depr.", "Exam Anxiety", "Screen Time"],
      datasets: [{ label: "Contribution %", data: [38.5, 32.0, 18.5, 11.0], backgroundColor: ["#ef4444", "#f97316", "#f59e0b", "#8b5cf6"] }]
    };
    new Chart(ctxFactors, { type: "bar", data: factorsConfig, options: { responsive: true, maintainAspectRatio: false, indexAxis: "y" } });
  }

  // 4. Fingerprint Radar Chart
  const ctxFingerprint = document.getElementById("dashFingerprintChart")?.getContext("2d");
  if (ctxFingerprint) {
    const fingerprintConfig = data?.fingerprint_chart || {
      labels: ["Academic", "Sleep Deficit", "Anxiety", "Screen", "Exercise Deficit", "Social Isolation"],
      datasets: [
        { label: "Student Profile", data: [8.5, 7.0, 7.5, 7.0, 6.5, 6.0], backgroundColor: "rgba(239, 68, 68, 0.25)", borderColor: "#ef4444" },
        { label: "Benchmark", data: [3.0, 1.0, 2.0, 2.5, 1.0, 1.5], backgroundColor: "rgba(16, 185, 129, 0.15)", borderColor: "#10b981" }
      ]
    };
    new Chart(ctxFingerprint, { type: "radar", data: fingerprintConfig, options: { responsive: true, maintainAspectRatio: false } });
  }

  // 5. Emotion Sentiment Doughnut
  const ctxEmotion = document.getElementById("dashEmotionChart")?.getContext("2d");
  if (ctxEmotion) {
    const emotionConfig = data?.emotion_chart || {
      labels: ["Optimistic", "Anxious", "Neutral"],
      datasets: [{ data: [25.0, 60.0, 15.0], backgroundColor: ["#10b981", "#ef4444", "#64748b"] }]
    };
    new Chart(ctxEmotion, { type: "doughnut", data: emotionConfig, options: { responsive: true, maintainAspectRatio: false } });
  }

  // 6. Activity Correlation Multi-bar Chart
  const ctxActivity = document.getElementById("dashActivityChart")?.getContext("2d");
  if (ctxActivity) {
    const activityConfig = data?.activity_chart || {
      labels: ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6"],
      datasets: [
        { label: "Sleep", data: [7.0, 6.5, 5.5, 6.0, 5.0, 4.5], backgroundColor: "#3b82f6" },
        { label: "Study", data: [4.0, 5.5, 7.0, 6.5, 8.0, 8.5], backgroundColor: "#8b5cf6" },
        { label: "Screen", data: [4.0, 5.0, 6.0, 5.5, 7.0, 7.5], backgroundColor: "#f43f5e" }
      ]
    };
    new Chart(ctxActivity, { type: "bar", data: activityConfig, options: { responsive: true, maintainAspectRatio: false } });
  }

  // 7. Recovery Progress Bar Chart
  const ctxRecoveryProgress = document.getElementById("dashRecoveryProgressChart")?.getContext("2d");
  if (ctxRecoveryProgress) {
    const recProgressConfig = data?.recovery_progress_chart || {
      labels: ["Box Breathing", "Digital Detox", "Pomodoro Break"],
      datasets: [
        { label: "Pre-Stress", data: [78.0, 82.0, 68.0], backgroundColor: "#ef4444" },
        { label: "Post-Stress", data: [52.0, 58.0, 42.0], backgroundColor: "#10b981" }
      ]
    };
    new Chart(ctxRecoveryProgress, { type: "bar", data: recProgressConfig, options: { responsive: true, maintainAspectRatio: false } });
  }

  // 8. Recovery Effectiveness Bar Chart
  const ctxRecoveryEff = document.getElementById("dashRecoveryEffectivenessChart")?.getContext("2d");
  if (ctxRecoveryEff) {
    const recEffConfig = data?.recovery_effectiveness_chart || {
      labels: ["4-7-8 Deep Box Breathing", "Bedtime Digital Detox", "Pomodoro Study Routine"],
      datasets: [{ label: "Effectiveness Score (%)", data: [92.5, 88.5, 84.0], backgroundColor: "#6366f1" }]
    };
    new Chart(ctxRecoveryEff, { type: "bar", data: recEffConfig, options: { responsive: true, maintainAspectRatio: false, indexAxis: "y" } });
  }
}