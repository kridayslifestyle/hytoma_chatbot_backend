def is_price_query(text: str):
    keywords = ["price", "cost", "₹", "budget", "offer", "pricing", "how much"]
    return any(k in text.lower() for k in keywords)


def is_product_query(text: str):
    """
    Only treat a message as a 'show me the product/price list' request
    when it's actually asking what's available or what something costs.
    A generic mention of a product noun (e.g. "installation process for
    smart door lock") should NOT trigger this — that must go to the
    LLM/RAG so it can answer the real question instead of dumping prices.
    """
    text = text.lower()

    listing_phrases = [
        "what do you have", "what type", "what types", "which types",
        "what options", "what models", "show me", "list of",
        "do you have", "types of"
    ]

    if any(p in text for p in listing_phrases):
        return True

    # Otherwise only route to the product list if it's clearly a
    # pricing question (handled by is_price_query) — don't fire on
    # bare product-category words alone.
    return False