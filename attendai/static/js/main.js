async function updateNavSessionBadge() {
  try {
    const res = await fetch("/api/session/status");
    const data = await res.json();
    const badge = document.getElementById("session-badge");
    const timerEl = document.getElementById("nav-timer");
    if (!badge) return;
    if (data.active && data.session) {
      badge.classList.remove("hidden");
      if (data.session.remaining_seconds != null) {
        const m = String(Math.floor(data.session.remaining_seconds / 60)).padStart(2, "0");
        const s = String(data.session.remaining_seconds % 60).padStart(2, "0");
        timerEl.textContent = m + ":" + s;
      }
    } else {
      badge.classList.add("hidden");
    }
  } catch (e) {}
}

setInterval(updateNavSessionBadge, 5000);
updateNavSessionBadge();
