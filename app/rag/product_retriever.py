import json
import os

# ---------------- ROOT PATH FIX ----------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PRODUCT_FILE = os.path.join(BASE_DIR, "products.json")


def load_products():
    try:
        with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("❌ Failed to load products.json:", e)
        print("Path used:", PRODUCT_FILE)
        return []


def retrieve_products(query: str):

    products = load_products()
    q = query.lower()

    results = []

    # ---------------- STRICT MATCH (CATEGORY + NAME) ----------------
    for category in products:
        cat_name = category.get("category", "").lower()

        for item in category.get("items", []):
            name = item.get("name", "").lower()

            # 🔥 STRICT MATCHING (IMPORTANT FIX)
            if cat_name in q or name in q:
                results.append({
                    "category": category["category"],
                    "name": item["name"],
                    "price": item["price"]
                })

    # ---------------- FALLBACK (CATEGORY ONLY) ----------------
    if not results:
        for category in products:
            if category["category"].lower() in q:
                for item in category["items"]:
                    results.append({
                        "category": category["category"],
                        "name": item["name"],
                        "price": item["price"]
                    })

    return results