import json
import os
import re

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


def extract_numbers(text: str):
    """Pull out standalone size/count numbers like '12', '6', '8-12' etc.
    Handles '12m' / '12 module' style shorthand by stripping trailing
    unit letters off a number token."""
    return set(re.findall(r"\d+", text))


def retrieve_products(query: str):

    products = load_products()

    q = normalize(query)
    query_numbers = extract_numbers(q)

    matched = []

    for category in products:
        cat_name = normalize(category["category"])

        category_items = []

        for item in category.get("items", []):

            name = normalize(item["name"])
            item_numbers = extract_numbers(name)

            # Match only when the full category name or full item name
            # appears in the query, or when the meaningful (non-stopword)
            # words overlap substantially — a single shared filler word
            # like "door" or "automation" is no longer enough on its own.
            query_words = set(q.split()) - STOPWORDS
            product_words = set((cat_name + " " + name).split()) - STOPWORDS

            overlap = query_words & product_words

            name_or_category_match = (
                cat_name in q
                or name in q
                or (product_words and overlap == product_words)
                or len(overlap) >= 2
            )

            if not name_or_category_match:
                continue

            category_items.append({
                "category": category["category"],
                "name": item["name"],
                "price": item["price"],
                "numbers": item_numbers,
            })

        if not category_items:
            continue

        if query_numbers:
            # The user asked for a specific size/count (e.g. "12 module",
            # "12m") — only return items whose own number matches. If
            # nothing in this category has that number, skip the whole
            # category instead of dumping every item in it.
            narrowed = [
                p for p in category_items
                if p["numbers"] & query_numbers
            ]
            matched.extend(narrowed)
        else:
            # No specific size mentioned — a general "what switch boards
            # do you have" style question, so the whole category is fine.
            matched.extend(category_items)

    return [
        {"category": p["category"], "name": p["name"], "price": p["price"]}
        for p in matched
    ]