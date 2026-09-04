document.addEventListener("DOMContentLoaded", async () => {
  let profile = null;
  const stored = localStorage.getItem("latest_stress_profile");

  if (stored) {
    try {
      profile = JSON.parse(stored);
    } catch (e) {
      console.warn("Error parsing stored stress profile", e);
    }
  }

  if (!profile) {
    profile = await ApiClient.getLatestStressProfile("STU_001");
  }

  renderResultPage(profile);
});

function renderResultPage(profile) {
  const score = parseFloat(profile.severity_score || 74.5).toFixed(1);
  const tier = profile.severity_tier || "High";
  const nature = profile.stress_nature || "Academic";
  const trajectory = profile.stress_trajectory || "Increasing";
  const factors = profile.major_factors || [];
  const explanation = profile.xai_explanation || "";
  const modelComp = profile.model_comparisons || {};

  // 1. Update Gauge & Score
  const gaugeScoreElem = document.getElementById("gaugeScore");
  if (gaugeScoreElem) gaugeScoreElem.textContent = score;

  // 2. Update Badges
  const tierBadge = document.getElementById("tierBadge");
  if (tierBadge) {
    tierBadge.textContent = `${tier} Severity`;
    if (tier === "Low") tierBadge.className = "badge badge-emerald";
    else if (tier === "Moderate") tierBadge.className = "badge badge-amber";
    else tierBadge.className = "badge badge-rose";
  }

  const natureBadge = document.getElementById("natureBadge");
  if (natureBadge) natureBadge.textContent = `${nature} Stress`;

  const trajectoryBadge = document.getElementById("trajectoryBadge");
  if (trajectoryBadge) trajectoryBadge.textContent = `Trajectory: ${trajectory}`;

  // 3. Update XAI Summary & Factors List
  const xaiSummaryElem = document.getElementById("xaiSummary");
  if (xaiSummaryElem) xaiSummaryElem.textContent = explanation;

  const factorsContainer = document.getElementById("xaiFactorsList");
  if (factorsContainer) {
    factorsContainer.innerHTML = "";
    
    factors.forEach(item => {
      const factorName = item.factor;
      const pct = parseFloat(item.percentage || 20.0).toFixed(1);

      const row = document.createElement("div");
      row.innerHTML = `
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.35rem;">
          <span style="color: var(--text-primary);">${factorName}</span>
          <span style="color: var(--accent-cyan);">${pct}%</span>
        </div>
        <div style="width: 100%; height: 8px; background: rgba(255, 255, 255, 0.08); border-radius: 4px; overflow: hidden;">
          <div style="width: ${pct}%; height: 100%; background: var(--accent-primary-gradient); border-radius: 4px; transition: width 0.8s ease;"></div>
        </div>
      `;
      factorsContainer.appendChild(row);
    });
  }

  // 4. Update Model Comparison Scores
  const dlVal = document.getElementById("dlScoreVal");
  if (dlVal) dlVal.textContent = parseFloat(modelComp.Multimodal_Fusion_DL || score).toFixed(1);

  const rfVal = document.getElementById("rfScoreVal");
  if (rfVal) rfVal.textContent = parseFloat(modelComp.Random_Forest_Baseline || (score * 0.98)).toFixed(1);

  const gbVal = document.getElementById("gbScoreVal");
  if (gbVal) gbVal.textContent = parseFloat(modelComp.Gradient_Boosting_Baseline || (score * 1.02)).toFixed(1);
}