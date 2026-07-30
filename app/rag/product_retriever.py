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

    for category in products:
        for item in category.get("items", []):

            name = item["name"].lower()
            category_name = category["category"].lower()

            if (
                any(word in name for word in q.split()) or
                any(word in category_name for word in q.split())
            ):
                results.append({
                    "category": category["category"],
                    "name": item["name"],
                    "price": item["price"]
                })

    # fallback → return full category if nothing matched
    if not results:
        for category in products:
            if any(word in category["category"].lower() for word in q.split()):
                for item in category["items"]:
                    results.append({
                        "category": category["category"],
                        "name": item["name"],
                        "price": item["price"]
                    })

    return results