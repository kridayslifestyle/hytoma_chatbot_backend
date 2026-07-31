import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PRODUCT_FILE = os.path.join(BASE_DIR, "products.json")


def load_products():
    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(text: str):
    return text.lower().replace("–", "-").replace("  ", " ")


def retrieve_products(query: str):

    products = load_products()

    q = normalize(query)

    results = []

    for category in products:
        cat_name = normalize(category["category"])

        for item in category.get("items", []):

            name = normalize(item["name"])

            # 🔥 SMART MATCH (VERY IMPORTANT FIX)

            query_words = set(q.split())
            product_words = set((cat_name + " " + name).split())

            if (
                cat_name in q
                or name in q
                or query_words & product_words
            ):
                results.append({
                    "category": category["category"],
                    "name": item["name"],
                    "price": item["price"]
                })

    return results