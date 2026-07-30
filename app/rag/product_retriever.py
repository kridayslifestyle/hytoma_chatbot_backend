import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PRODUCT_FILE = os.path.join(BASE_DIR, "data", "products.json")


def load_products():
    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def retrieve_products(query: str):

    products = load_products()
    q = query.lower()

    results = []

    # ---------------- SMART MATCH ----------------
    for category in products:
        category_name = category["category"].lower()

        for item in category.get("items", []):
            item_name = item["name"].lower()

            # ✅ match ANY keyword in category OR product name
            if (
                any(word in item_name for word in q.split()) or
                any(word in category_name for word in q.split())
            ):
                results.append({
                    "category": category["category"],
                    "name": item["name"],
                    "price": item["price"]
                })

    # ---------------- FALLBACK ----------------
    if not results:

        # try category-level fallback
        for category in products:
            if any(word in category["category"].lower() for word in q.split()):
                for item in category["items"]:
                    results.append({
                        "category": category["category"],
                        "name": item["name"],
                        "price": item["price"]
                    })

    return results