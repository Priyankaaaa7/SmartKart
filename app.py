from flask import Flask, render_template, request, jsonify
from spoilt_guard import (
    load_customer_data,
    save_customer_data,
    get_expiring_items,
    suggest_live_recipes,
    mark_item_used,
    check_badges
)

app = Flask(__name__)

# Home extension popup
@app.route("/")
def home():
    return render_template("index.html")

# Mock grocery shopping site
@app.route("/mock-store")
def mock_store():
    return render_template("clone.html")

# Budget page
@app.route("/budget")
def budget():
    data = load_customer_data()
    return render_template("budget.html", budget=data["budget"])

# Update budget when user adds item from store
@app.route("/update-budget", methods=["POST"])
def update_budget():
    data = load_customer_data()
    item = request.get_json()

    if item:
        try:
            cost = float(item.get("price", 0))
            data["budget"]["currentSpent"] += cost
            save_customer_data(data)
            return jsonify({"status": "success", "newSpent": data["budget"]["currentSpent"]}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    return jsonify({"status": "error", "message": "Invalid item data"}), 400

# View expiry tracker
@app.route("/expiry")
def expiry_tracker():
    data = load_customer_data()
    items = get_expiring_items(data["pantry"])
    return render_template("expiry.html", items=items)

# View recipe suggestions
@app.route("/recipes")
def recipe_suggestions():
    data = load_customer_data()
    recipes = suggest_live_recipes(data["pantry"])
    return render_template("recipes.html", recipes=recipes)

@app.route("/pantry")
def virtual_pantry():
    data = load_customer_data()
    return render_template("pantry.html", pantry=data["pantry"])

# View badges
@app.route("/badges")
def badges():
    data = load_customer_data()
    return render_template("badges.html", count=data["savedFromExpiryCount"], badges=data["badgesEarned"])

# Just for testing: get current budget as JSON
@app.route("/api/budget")
def api_budget():
    data = load_customer_data()
    return jsonify(data["budget"])

import matplotlib.pyplot as plt
import io
import base64

@app.route("/summary-graph")
def summary_graph():
    data = load_customer_data()
    pantry = data["pantry"]

    # Budget chart data
    spent = data["budget"]["currentSpent"]
    remaining = max(0, data["budget"]["monthly"] - spent)

    # Pantry status breakdown
    status_counts = {
        "active": 0,
        "expiring_soon": 0,
        "near_expiry": 0,
        "used": 0
    }
    for item in pantry:
        status = item["status"]
        if status in status_counts:
            status_counts[status] += 1

    # Create matplotlib figure
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    plt.tight_layout()

    # Pie chart (budget)
    axs[0].pie(
        [spent, remaining],
        labels=["Spent", "Remaining"],
        autopct="%1.1f%%",
        colors=["#3b82f6", "#a7f3d0"]
    )
    axs[0].set_title("💸 Budget Usage")

    # Bar chart (pantry status)
    axs[1].bar(
        status_counts.keys(),
        status_counts.values(),
        color=["#60a5fa", "#facc15", "#f97316", "#9ca3af"]
    )
    axs[1].set_title("📦 Pantry Item Status")

    # Save to PNG in memory
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf.read(), 200, {"Content-Type": "image/png"}
@app.route("/summary")
def summary():
    data = load_customer_data()
    pantry = data["pantry"]
    expiring_count = sum(1 for item in pantry if item["status"] in ["expiring_soon", "near_expiry"])
    used_count = sum(1 for item in pantry if item["status"] == "used")

    return render_template("summary.html",
                           budget=data["budget"],
                           pantry=pantry,
                           expiring_count=expiring_count,
                           used_count=used_count,
                           savedFromExpiryCount=data["savedFromExpiryCount"],
                           badges=data["badgesEarned"],
                           graph_url="/summary-graph")
@app.route("/mark-used", methods=["POST"])
def mark_used():
    data = load_customer_data()
    req = request.get_json()
    item_name = req.get("item")

    if item_name:
        updated = mark_item_used(data, item_name)
        save_customer_data(updated)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid item"}), 400


if __name__ == "__main__":
    app.run(debug=True)
