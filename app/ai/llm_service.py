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

    # ---------------- PRODUCT FETCH ----------------
    products = retrieve_products(question)

    # FORCE JSON SAFE FORMAT
    context = json.dumps(products, indent=2)

    print("\n====================")
    print("QUESTION:", question)
    print("\nPRODUCT CONTEXT:")
    print(context)
    print("====================\n")

    # ---------------- STRICT SYSTEM PROMPT ----------------
    system_prompt = """
You are Hytoma AI, a STRICT sales assistant for Hytoma Automation LLP.

🔥 CRITICAL RULES (NON-NEGOTIABLE):

1. NEVER create bundles or combinations
2. NEVER mix multiple products into one offer
3. NEVER modify prices
4. NEVER assume budget or customer intent
5. NEVER generate new products
6. ONLY use the given product catalog

📦 OUTPUT RULE:
- Show ONLY matching products
- Format:
  Product Name: ₹Price
- Use bullet points only (-)
- No paragraphs

💰 PRICE RULE:
- Use EXACT prices from catalog
- If not found → say:
  "Please contact Hytoma for best price & details."

📌 IMPORTANT LINE (MANDATORY):
Always end response with:
"For best price contact us"

STYLE:
- Short
- Simple Instagram tone
- Sales executive style
- No explanations
"""

    # ---------------- MESSAGE BUILD ----------------
    messages_payload = [
        {
            "role": "system",
            "content": system_prompt + "\n\nPRODUCT CATALOG:\n" + context
        }
    ] + messages

    # ---------------- LLM CALL ----------------
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=messages_payload
    )

    reply = response.choices[0].message.content

    # ---------------- SAFETY CUT ----------------
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