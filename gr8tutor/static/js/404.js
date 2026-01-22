(() => {
  // Seconds before redirect
  const REDIRECT_SECONDS = 5;

  const countdownEl = document.getElementById("countdown");
  let remaining = REDIRECT_SECONDS;

  const interval = setInterval(() => {
    remaining--;

    if (countdownEl) {
      countdownEl.textContent = remaining;
    }

    if (remaining <= 0) {
      clearInterval(interval);
      window.location.href = "/";
    }
  }, 1000);
})();
