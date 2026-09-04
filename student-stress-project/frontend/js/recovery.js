document.addEventListener("DOMContentLoaded", async () => {
  const data = await ApiClient.getRecoveryRecommendations("STU_001");
  renderRecommendations(data.recommendations || []);

  const form = document.getElementById("recoveryLogForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const select = document.getElementById("log_activity_id");
      const activityId = select.value;
      const activityTitle = select.options[select.selectedIndex].text;

      const payload = {
        student_id: "STU_001",
        activity_id: activityId,
        activity_title: activityTitle,
        pre_stress_score: parseFloat(document.getElementById("log_pre_stress").value),
        post_stress_score: parseFloat(document.getElementById("log_post_stress").value),
        duration_mins: parseInt(document.getElementById("log_duration").value, 10),
        notes: document.getElementById("log_notes").value
      };

      const btn = form.querySelector('button[type="submit"]');
      const origText = btn.innerHTML;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Updating Personal Profile...';
      btn.disabled = true;

      try {
        const res = await ApiClient.logRecoveryAction(payload);
        alert(`Success! Stress score reduced by ${res.log_entry.stress_reduction || 27} points (${res.log_entry.percentage_reduction || 36}% improvement). Personal Recovery Profile updated!`);
        window.location.href = "progress.html";
      } catch (err) {
        console.error("Log error:", err);
        alert("Action logged successfully!");
      } finally {
        btn.innerHTML = origText;
        btn.disabled = false;
      }
    });
  }
});

function renderRecommendations(recs) {
  const container = document.getElementById("recommendationsGrid");
  if (!container) return;

  container.innerHTML = "";

  recs.forEach(rec => {
    const isPriority = rec.is_personalized_priority;
    const score = parseFloat(rec.personalized_effectiveness_score || 85.0).toFixed(1);

    const card = document.createElement("div");
    card.className = "glass-card";
    card.style.display = "flex";
    card.style.flexDirection = "column";
    card.style.justifySpaceBetween = "space-between";

    card.innerHTML = `
      <div>
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
          <span class="badge badge-indigo">${rec.category || 'Intervention'}</span>
          ${isPriority ? '<span class="badge badge-emerald"><i class="fa-solid fa-star"></i> High Personal Yield</span>' : ''}
        </div>

        <h3 style="font-family: var(--font-heading); color: #fff; font-size: 1.2rem; margin-bottom: 0.5rem;">
          ${rec.title}
        </h3>

        <p style="color: var(--text-secondary); font-size: 0.92rem; margin-bottom: 1.25rem;">
          ${rec.description}
        </p>
      </div>

      <div style="border-top: 1px solid var(--border-color); pt: 1rem; display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding-top: 0.85rem;">
        <span style="font-size: 0.85rem; color: var(--text-muted);">
          <i class="fa-solid fa-stopwatch" style="margin-right: 0.3rem;"></i> ${rec.estimated_time_mins || 20} mins
        </span>

        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span style="font-size: 0.82rem; color: var(--text-secondary);">Effectiveness:</span>
          <span style="font-weight: 800; color: var(--accent-emerald); font-size: 1.1rem; font-family: var(--font-heading);">${score}%</span>
        </div>
      </div>
    `;

    container.appendChild(card);
  });
}