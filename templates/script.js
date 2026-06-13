const BASE_URL = "https://thorough-charm-production-0fbe.up.railway.app";

// Budget
document.getElementById("budgetBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: `${BASE_URL}/budget` });
});

// Pantry
document.getElementById("pantryBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: `${BASE_URL}/pantry` });
});

// Summary
document.getElementById("insightBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: `${BASE_URL}/summary` });
});

// Spoilt Guard dropdown toggle
document.getElementById("spoiltBtn").addEventListener("click", () => {
  const submenu = document.getElementById("spoiltSubmenu");
  submenu.classList.toggle("open");
});

// Expiry Tracker
document.getElementById("expiryBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: `${BASE_URL}/expiry` });
});

// Recipes
document.getElementById("cookBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: `${BASE_URL}/recipes` });
});

// Badges
document.getElementById("badgesBtn").addEventListener("click", () => {
  chrome.tabs.create({ url: `${BASE_URL}/badges` });
});
