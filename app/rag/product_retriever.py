import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PRODUCT_FILE = os.path.join(BASE_DIR, "products.json")


def load_products():
    with open(PRODUCT_FILE, "r") as f:
        return json.load(f)


def retrieve_products(query: str):
    products = load_products()

    result = []

    query = query.lower()

    for category in products:
        for item in category["items"]:
            if query in item["name"].lower() or query in category["category"].lower():
                result.append(item)

    return result