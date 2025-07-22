import json
import requests
from datetime import datetime

API_KEY = "27f8b76b350e449d95b150d6a3d15c2a"

# Load pantry data
def load_customer_data(path="customerData.json"):
    with open(path, "r") as f:
        return json.load(f)

# Save pantry data
def save_customer_data(data, path="customerData.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Check for items expiring in 0–2 days
def get_expiring_items(pantry):
    today = datetime.today().date()
    expiring = []

    for item in pantry:
        try:
            expiry = datetime.strptime(item["estimatedExpiry"], "%Y-%m-%d").date()
            days_left = (expiry - today).days
            item["daysLeft"] = days_left

            if 0 <= days_left <= 7 and item["status"] != "used":
                expiring.append(item)
        except Exception as e:
            print(f"⚠️ Error parsing expiry for {item['item']}: {e}")

    return expiring

# Suggest recipes using Spoonacular API
def suggest_live_recipes(pantry):
    seen = set()
    ingredients = []

    for item in pantry:
        name = item["item"].strip().lower()
        if item["status"] != "used" and name not in seen:
            seen.add(name)
            ingredients.append(name)

    if not ingredients:
        return []

    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ",".join(ingredients),
        "number": 5,
        "ranking": 1,
        "ignorePantry": True,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        with open("spoonacular_response.json", "w") as f:
            json.dump(data, f, indent=2)

        return [
            {
                "name": r.get("title", "Unknown"),
                "image": r.get("image", ""),
                "usedIngredients": r.get("usedIngredientCount", 0),
                "missedIngredients": r.get("missedIngredientCount", 0),
                "missedIngredientNames": [i.get("name") for i in r.get("missedIngredients", [])]
            }
            for r in data
        ]
    else:
        print("❌ Spoonacular API Error:", response.status_code, response.text)
        return []


# Mark an item as used
def mark_item_used(data, item_name):
    for item in data["pantry"]:
        if item["item"].lower() == item_name.lower() and item["status"] != "used":
            item["used"] += 1
            if item["used"] >= item["quantity"]:
                item["status"] = "used"
                data["savedFromExpiryCount"] += 1
    return data

# Check and unlock badge
def check_badges(data):
    badge_criteria = {
        10: "Food Saver 🥕",
        25: "Zero Waste Hero ♻️",
        50: "No-Waste Warrior 🛡️",
        100: "Expiry Slayer ⚔️"
    }

    unlocked = []

    for threshold, name in badge_criteria.items():
        if data["savedFromExpiryCount"] >= threshold and name not in data["badgesEarned"]:
            data["badgesEarned"].append(name)
            unlocked.append(name)

    return unlocked  # list of newly unlocked

# CLI Debugging
if __name__ == "__main__":
    data = load_customer_data()
    pantry = data["pantry"]

    print("📦 Expiring Items:")
    expiring = get_expiring_items(pantry)
    if expiring:
        for item in expiring:
            print(f"- {item['item']} (⏳ {item['daysLeft']} days left)")
    else:
        print("🎉 Nothing is expiring soon!")

    print("\n🍽️ Suggested Recipes:")
    suggestions = suggest_live_recipes(pantry)
    for s in suggestions:
        print(f"- {s['name']} (Used: {s['usedIngredients']} | Missing: {s['missedIngredients']})")

    data = mark_item_used(data, "Milk")
    badge = check_badges(data)
    if badge:
        print("🏅", badge)

    save_customer_data(data)
