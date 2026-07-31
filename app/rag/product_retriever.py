import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PRODUCT_FILE = os.path.join(BASE_DIR, "products.json")

# Generic words that show up across multiple categories/items and must
# never be used, on their own, to decide a match (this was the root
# cause of "gate automation" pulling in curtain motors, and "door lock"
# pulling in video doorbells — they all share a word like "automation"
# or "door").
STOPWORDS = {
    "the", "a", "an", "of", "for", "and", "or", "to", "in", "on",
    "with", "what", "which", "you", "your", "have", "do", "does",
    "is", "are", "type", "types", "price", "cost", "smart",
}


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

            # Match only when the full category name or full item name
            # appears in the query, or when the meaningful (non-stopword)
            # words overlap substantially — a single shared filler word
            # like "door" or "automation" is no longer enough on its own.
            query_words = set(q.split()) - STOPWORDS
            product_words = set((cat_name + " " + name).split()) - STOPWORDS

            overlap = query_words & product_words

            if (
                cat_name in q
                or name in q
                or (product_words and overlap == product_words)
                or len(overlap) >= 2
            ):
                results.append({
                    "category": category["category"],
                    "name": item["name"],
                    "price": item["price"]
                })

    return results