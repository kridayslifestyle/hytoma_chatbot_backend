def is_price_query(text: str):
    keywords = ["price", "cost", "₹", "budget", "offer", "pricing"]
    return any(k in text.lower() for k in keywords)


def is_product_query(text: str):
    keywords = [
        "lock", "motor", "gate", "curtain",
        "switch", "doorbell", "sensor",
        "automation", "types", "what do you have"
    ]
    return any(k in text.lower() for k in keywords)