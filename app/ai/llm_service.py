from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from app.rag.product_retriever import retrieve_products

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ---------------- PRICE QUERY DETECTOR ----------------
def is_price_query(text: str):
    keywords = [
        "price", "cost", "₹", "rs", "budget",
        "offer", "rate", "how much", "pricing"
    ]
    return any(k in text.lower() for k in keywords)


# ---------------- MAIN RESPONSE ----------------
def generate_reply(messages):

    question = messages[-1]["content"].strip()

    products = retrieve_products(question)

    # ✅ FIXED FORMAT (NO JSON)
    def format_products(products):
        if not products:
            return ""

        return "\n".join([
            f"- {p['name']}: ₹{p['price']}"
            for p in products
        ])

    context = format_products(products)

    print("\nQUESTION:", question)
    print("\nPRODUCT CONTEXT:\n", context)

    system_prompt = """
You are Hytoma AI Sales Assistant.

🚨 RULES:
- NEVER mix products
- NEVER create bundles
- NEVER modify prices
- ONLY use given product list

📦 FORMAT:
- Product Name: ₹Price

IF NO PRODUCTS:
Say: "Please contact Hytoma for best price & details."

Always end with:
"For best price contact us"
"""

    messages_payload = [
        {
            "role": "system",
            "content": system_prompt + "\n\nPRODUCTS:\n" + context
        }
    ] + messages

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=messages_payload
    )

    reply = response.choices[0].message.content

    if len(reply) > 950:
        reply = reply[:950].rsplit(" ", 1)[0] + "..."

    return reply


# ---------------- SUMMARY ENGINE ----------------
def generate_summary(messages):

    conversation = ""

    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {
                "role": "system",
                "content": """
You are a memory engine.

Create a SHORT summary of conversation.

RULES:
- Only factual data
- No recommendations
- No opinions
- Under 100 words
"""
            },
            {
                "role": "user",
                "content": conversation
            }
        ]
    )

    summary = response.choices[0].message.content

    if not summary:
        return None

    return summary.strip()