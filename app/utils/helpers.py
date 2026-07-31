def is_product_query(text: str):
    keywords = [
        "lock", "motor", "gate", "curtain",
        "switch", "doorbell", "sensor",
        "automation", "what do you have", "types"
    ]

    t = text.lower()
    return any(k in t for k in keywords)