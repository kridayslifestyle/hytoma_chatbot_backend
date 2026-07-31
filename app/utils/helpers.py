def is_price_query(text: str):
    keywords = ["price", "cost", "₹", "budget", "offer", "pricing"]
    return any(k in text.lower() for k in keywords)