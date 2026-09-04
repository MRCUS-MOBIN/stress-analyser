document.addEventListener("DOMContentLoaded", () => {
  const anxietySlider = document.getElementById("anxiety_level");
  const anxietyVal = document.getElementById("anxietyVal");

  const moodSlider = document.getElementById("mood_rating");
  const moodVal = document.getElementById("moodVal");

  const routineSlider = document.getElementById("routine_consistency_score");
  const routineVal = document.getElementById("routineVal");

  if (anxietySlider && anxietyVal) {
    anxietySlider.addEventListener("input", (e) => anxietyVal.textContent = parseFloat(e.target.value).toFixed(1));
  }
  if (moodSlider && moodVal) {
    moodSlider.addEventListener("input", (e) => moodVal.textContent = parseFloat(e.target.value).toFixed(1));
  }
  if (routineSlider && routineVal) {
    routineSlider.addEventListener("input", (e) => routineVal.textContent = parseFloat(e.target.value).toFixed(1));
  }

  const form = document.getElementById("assessmentForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const assessmentPayload = {
        student_id: "STU_001",
        anxiety_level: parseFloat(anxietySlider.value),
        mood_rating: parseFloat(moodSlider.value),
        routine_consistency_score: parseFloat(routineSlider.value),
        sleep_hours: parseFloat(document.getElementById("sleep_hours").value),
        study_hours: parseFloat(document.getElementById("study_hours").value),
        screen_time_hours: parseFloat(document.getElementById("screen_time_hours").value),
        physical_activity_mins: parseFloat(document.getElementById("physical_activity_mins").value),
        academic_workload_score: parseFloat(document.getElementById("academic_workload_score").value),
        social_activity_hours: parseFloat(document.getElementById("social_activity_hours").value),
        journal_entry: document.getElementById("journal_entry").value
      };

      const btn = form.querySelector('button[type="submit"]');
      const originalText = btn.innerHTML;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Your Stress Level...';
      btn.disabled = true;

      try {
        const response = await ApiClient.submitAssessment(assessmentPayload);
        localStorage.setItem("latest_stress_profile", JSON.stringify(response.stress_profile || response));
        window.location.href = "result.html";
      } catch (err) {
        console.error("Submission error:", err);
        alert("Failed to submit assessment. Please check backend status.");
      } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    });
  }
});

function fillJournal(text) {
  const textarea = document.getElementById("journal_entry");
  if (textarea) {
    textarea.value = text;
  }
}