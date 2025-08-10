// Open Flask routes in tabs
document.getElementById("budgetBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: "http://127.0.0.1:5000/budget" });
});

document.getElementById("suggestBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: "http://127.0.0.1:5000/suggestions" });
});

document.getElementById("insightBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: "http://127.0.0.1:5000/insights" });
});

// Spoilt Guard dropdown toggle
document.getElementById("spoiltBtn").addEventListener("click", () => {
  const submenu = document.getElementById("spoiltSubmenu");
  submenu.classList.toggle("hidden");
});

// Spoilt Guard submenu actions
document.getElementById("expiryBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: "http://127.0.0.1:5000/expiry" });
});
document.getElementById("cookBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: "http://127.0.0.1:5000/recipes" });
});
document.getElementById("badgesBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: "http://127.0.0.1:5000/badges" });
});
