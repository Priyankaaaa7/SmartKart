document.getElementById("budgetBtn").addEventListener("click", () => {
  window.open("http://127.0.0.1:5000/budget", "_blank");
});

document.getElementById("pantryBtn").addEventListener("click", () => {
  window.open("http://127.0.0.1:5000/pantry", "_blank");
});

document.getElementById("insightBtn").addEventListener("click", () => {
  window.open("http://127.0.0.1:5000/summary", "_blank");
});

document.getElementById("spoiltBtn").addEventListener("click", () => {
  document.getElementById("spoiltSubmenu").classList.toggle("open");
});

document.getElementById("expiryBtn").addEventListener("click", () => {
  window.open("http://127.0.0.1:5000/expiry", "_blank");
});

document.getElementById("cookBtn").addEventListener("click", () => {
  window.open("http://127.0.0.1:5000/recipes", "_blank");
});

document.getElementById("badgesBtn").addEventListener("click", () => {
  window.open("http://127.0.0.1:5000/badges", "_blank");
});
