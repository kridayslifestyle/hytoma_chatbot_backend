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


def generate_reply(messages):

    question = messages[-1]["content"]

    # ---------------- PRODUCT DATA ----------------
    products = retrieve_products(question)

    # 🔥 ALWAYS FORMAT PROPERLY (VERY IMPORTANT FIX)
    context = json.dumps(products, indent=2)

    print("\nQuestion:")
    print(question)

    print("\nPRODUCT CONTEXT:")
    print(context)

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {
                "role": "system",
                "content": f"""
You are Hytoma AI, a professional sales assistant for Hytoma Automation LLP.

PRODUCT CATALOG (STRICT - USE ONLY THIS):

{context}

RULES (VERY IMPORTANT):

- Reply must be under 120 words
- Be short, clear, and sales focused
- Use bullet points (-) when needed
- Do NOT invent or modify prices
- NEVER change MRP values
- Only use product catalog above
- If not in catalog, say:
  "Please contact Hytoma for best price & details."

IMPORTANT:
Always mention: "For best price contact us"

STYLE:
- Friendly sales executive tone
- Simple Instagram language
- No technical explanations
"""
            }
        ] + messages,
    )

    reply = response.choices[0].message.content

    # ---------------- SAFETY LIMIT ----------------
    if len(reply) > 950:
        reply = reply[:950].rsplit(" ", 1)[0] + "..."

    return reply