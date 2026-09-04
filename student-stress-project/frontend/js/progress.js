document.addEventListener("DOMContentLoaded", async () => {
  const dashData = await ApiClient.getDashboardData("STU_001");

  renderProgressCharts(dashData);
  renderEffectivenessTable();
});

function renderProgressCharts(dashData) {
  const ctxTrend = document.getElementById("progressTrendChart")?.getContext("2d");
  if (ctxTrend) {
    const trendConfig = dashData?.trend_chart || {
      labels: ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6"],
      datasets: [
        {
          label: "Student Stress Trajectory",
          data: [52.0, 58.0, 64.0, 61.0, 71.0, 74.5],
          borderColor: "#6366f1",
          backgroundColor: "rgba(99, 102, 241, 0.15)",
          fill: true,
          tension: 0.4
        },
        {
          label: "Optimal Threshold",
          data: [50, 50, 50, 50, 50, 50],
          borderColor: "#10b981",
          borderDash: [5, 5],
          fill: false
        }
      ]
    };
    new Chart(ctxTrend, { type: "line", data: trendConfig, options: { responsive: true, maintainAspectRatio: false } });
  }

  const ctxPrePost = document.getElementById("prePostChart")?.getContext("2d");
  if (ctxPrePost) {
    const prePostConfig = dashData?.recovery_progress_chart || {
      labels: ["Box Breathing", "Digital Detox", "Pomodoro Break", "Cardio Walk"],
      datasets: [
        { label: "Pre-Intervention", data: [78.0, 82.0, 68.0, 75.0], backgroundColor: "#ef4444" },
        { label: "Post-Intervention", data: [52.0, 58.0, 42.0, 48.0], backgroundColor: "#10b981" }
      ]
    };
    new Chart(ctxPrePost, { type: "bar", data: prePostConfig, options: { responsive: true, maintainAspectRatio: false } });
  }
}

function renderEffectivenessTable() {
  const tbody = document.getElementById("effectivenessTableBody");
  if (!tbody) return;

  const sampleRows = [
    { title: "4-7-8 Deep Diaphragmatic Box Breathing", count: 4, red: 26.5, pct: 35.3, score: 92.5 },
    { title: "90-Min Bedtime Digital Detox", count: 3, red: 24.0, pct: 31.0, score: 88.5 },
    { title: "Structured Pomodoro Study & Break Routine", count: 5, red: 22.0, pct: 28.5, score: 84.0 },
    { title: "30-Min Aerobic Physical Activity", count: 2, red: 21.0, pct: 27.0, score: 82.0 }
  ];

  tbody.innerHTML = "";
  sampleRows.forEach(row => {
    const tr = document.createElement("tr");
    tr.style.borderBottom = "1px solid var(--border-color)";

    tr.innerHTML = `
      <td style="padding: 0.85rem 1rem; font-weight: 600; color: #fff;">${row.title}</td>
      <td style="padding: 0.85rem 1rem; color: var(--text-secondary);">${row.count} times</td>
      <td style="padding: 0.85rem 1rem; color: var(--accent-rose); font-weight: 700;">-${row.red} pts</td>
      <td style="padding: 0.85rem 1rem; color: var(--accent-cyan); font-weight: 700;">${row.pct}%</td>
      <td style="padding: 0.85rem 1rem; color: var(--accent-emerald); font-weight: 800; font-family: var(--font-heading); font-size: 1.05rem;">${row.score}%</td>
    `;
    tbody.appendChild(tr);
  });
}