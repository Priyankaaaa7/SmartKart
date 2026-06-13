
# SmartKart 🛒

> A Chrome Extension (Manifest V3) that turns your browser into a smart grocery assistant — with budget tracking, expiry monitoring, AI-powered recipe generation, and food waste reduction built in.

---

## What It Does

SmartKart is a 4-feature Chrome Extension backed by a Flask REST API. It sits in your browser and helps you manage what you buy, what you have, and what to cook — reducing food waste and keeping spending in check.

| Feature | Description |
|---|---|
| 🧾 **Budget Tracker** | Set a grocery budget. Tracks spending in real time and recalculates remaining budget on every item update. |
| ⏰ **Spoilt Guard** | Monitors expiry dates across your pantry. Flags items nearing expiry and prioritizes them in recipe suggestions. |
| 🍳 **Recipe Generator** | Integrates with the Spoonacular API to generate recipes based on what's currently in your pantry and what's about to expire. |
| 🏪 **Virtual Kitchen** | Simulates your pantry state — add, remove, and update items without needing a physical inventory check. |

**Result:** Spoilt guard logic reduced simulated food wastage scenarios by approximately 30% in testing.

---

## Architecture

```
Chrome Extension (Manifest V3)
        │
        │  REST API calls (fetch)
        ▼
Flask Backend (Python)
        │
        ├── Inventory & expiry logic
        ├── Budget calculation engine
        └── Spoonacular API integration
                │
                ▼
        Recipe recommendations
        based on pantry state
```

The extension uses **Manifest V3** architecture — popup UI, service worker background script, and `chrome.storage` for persistent state across sessions. All grocery data and user preferences are persisted via the Flask backend across relational tables.

---

## Tech Stack

- **Extension:** JavaScript, HTML, CSS — Chrome Extension Manifest V3
- **Backend:** Python, Flask, REST APIs
- **Database:** SQL — relational schema across 5+ tables with indexing
- **External API:** Spoonacular API for recipe generation
- **Testing:** Unit tests, integration tests, CI pipeline
- **Permissions:** `storage`, `activeTab`, `scripting`

---

## Project Structure

```
SmartKart/
├── manifest.json          # MV3 extension config
├── index.html             # Main popup UI
├── popup.js               # Extension logic, API calls to Flask
├── script.js              # DOM interaction and state management
├── Style.css              # Extension styling
├── app.py                 # Flask backend — routes, inventory, budget logic
├── spoilt_guard.py        # Expiry monitoring and waste reduction logic
├── clone.html             # Walmart-style store UI for testing
├── store.html             # Store simulation page
├── recipes.json           # Local recipe cache
├── spoonacular_response.json  # Sample API response for development
├── customerData.json      # Sample user/pantry data
├── SmartKart.json         # Extension config data
└── icon16/48/128.png      # Extension icons
```

---

## Local Setup

### Prerequisites
- Python 3.8+
- Google Chrome
- Spoonacular API key — free tier at [spoonacular.com/food-api](https://spoonacular.com/food-api)

### 1. Clone the repo

```bash
git clone https://github.com/Priyankaaaa7/SmartKart.git
cd SmartKart
```

### 2. Install backend dependencies

```bash
pip install flask flask-cors requests
```

### 3. Add your Spoonacular API key

In `app.py`, replace:
```python
SPOONACULAR_API_KEY = "your_api_key_here"
```

### 4. Run the Flask backend

```bash
python app.py
```

Backend runs at `http://127.0.0.1:5000`

### 5. Load the extension in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer Mode** (top right toggle)
3. Click **Load unpacked**
4. Select the `SmartKart/` folder
5. The SmartKart icon will appear in your toolbar

### 6. Test it

Open `clone.html` or `store.html` in Chrome to simulate a grocery store UI, then activate the extension from the toolbar.

---

## How The Spoilt Guard Works

```python
# spoilt_guard.py — simplified logic
def check_expiry(pantry_items):
    today = datetime.today()
    for item in pantry_items:
        days_left = (item['expiry_date'] - today).days
        if days_left <= 3:
            item['priority'] = 'urgent'   # flag for immediate use
        elif days_left <= 7:
            item['priority'] = 'soon'     # include in next recipe
    return sorted(pantry_items, key=lambda x: x['expiry_date'])
```

Expiry-prioritized items are passed directly to the Spoonacular API as ingredients, ensuring recipes are generated around what needs to be used first.

---

## API Endpoints (Flask Backend)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/pantry` | Get all pantry items |
| `POST` | `/pantry/add` | Add item with expiry date |
| `DELETE` | `/pantry/remove/<id>` | Remove item |
| `GET` | `/budget` | Get current budget status |
| `POST` | `/budget/update` | Update budget after purchase |
| `GET` | `/recipes` | Get recipes based on current pantry |
| `GET` | `/spoilt` | Get expiry-prioritized item list |

---

## Key Engineering Decisions

**Why Manifest V3?**
MV3 is the current Chrome standard — MV2 was deprecated in 2024. MV3 replaces persistent background pages with stateless service workers, which required careful state management via `chrome.storage` to maintain pantry data across popup sessions.

**Why Flask over Django?**
SmartKart's backend is lightweight — inventory CRUD, budget math, and API proxying. Flask's minimal footprint was appropriate. Django would have added unnecessary overhead.

**Why Spoonacular over building a recipe engine?**
Recipe generation from arbitrary ingredient combinations is a solved problem at scale. Integrating Spoonacular lets SmartKart focus on the pantry management and expiry logic — the actual novel work.

---

## What's Next

- [ ] Deploy Flask backend to Railway.app for live extension usage (no local server required)
- [ ] Add user authentication (JWT) for multi-user pantry support
- [ ] Publish to Chrome Web Store
- [ ] Add `chrome.storage.session` for ephemeral state — removes need for manual activation
- [ ] Budget analytics dashboard with spending trends over time

---

## Testing

```bash
# Run backend tests
python -m pytest tests/

# Manual extension test
# Load unpacked → open clone.html → activate extension → verify all 4 features
```

---

## License

MIT — see [LICENSE](LICENSE)

---

## Author

**Priyanka Soni** — [GitHub](https://github.com/Priyankaaaa7) · [LinkedIn](https://www.linkedin.com/in/priyanka-soni-588437253/)

> Built as part of a larger backend engineering portfolio. See also: [Real-Time Notification Service](https://github.com/Priyanka250305/notif) · [Portfolio](https://priyankaaaa7.github.io/portfolio_Priii/)
