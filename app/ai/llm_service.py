from openai import OpenAI
from dotenv import load_dotenv
import os

from app.rag.retriever import retrieve_context
from app.utils.constants import MAX_HISTORY, SUMMARY_TRIGGER, SYSTEM_PROMPT
from app.rag.product_retriever import retrieve_products

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY")
)


def generate_reply(messages):

    question = messages[-1]["content"]

    products = retrieve_products(question)

    context = f"""
    PRODUCT CATALOG (USE ONLY THIS):

    {products}
    """

    print("\nQuestion:")
    print(question)

    print("\nRetrieved Context:")
    print(context)

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {
                "role": "system",
                "content": f"""
You are Hytoma AI, a professional sales assistant for Hytoma Automation LLP.

Use ONLY the knowledge base below:

{context}

RULES (VERY IMPORTANT):

- Reply must be under 120 words.
- Be short, clear, and direct.
- Use simple Instagram-friendly language.
- Use bullet points (-) when needed.
- Do NOT write long paragraphs.
- Do NOT mention "knowledge base", "context", or "documents".
- Do NOT say "based on" or "according to".
- Do NOT use outside knowledge.
- Do NOT explain reasoning.

IMPORTANT:
- These are official company prices
- NEVER modify prices
- NEVER generate new prices
- If user asks for price, only use this catalog
- Always mention: "For best price contact us"

STYLE:

- Human sales executive tone
- Friendly and professional
- Natural conversation

If answer is not in context, say:
"Please contact Hytoma for more details."
""",
            }
        ]
        + messages,
    )

    reply = response.choices[0].message.content

    # FINAL SAFETY (prevents Instagram 1000-char error)
    if len(reply) > 950:
        reply = reply[:950].rsplit(" ", 1)[0] + "..."

    return reply


def generate_summary(messages):

    conversation = ""

    for msg in messages:

        conversation += f"{msg['role']}: " f"{msg['content']}\n"

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {
                "role": "system",
                "content": """
You are a memory engine.

Create a concise summary of this conversation.

Preserve:

- customer interests
- products discussed
- preferences
- decisions made
- important facts
- contact details if mentioned

Rules:

- Return only factual information.
- Do not answer the customer.
- Do not make recommendations.
- Keep the summary under 100 words.
""",
            },
            {"role": "user", "content": conversation},
        ],
    )

    summary = response.choices[0].message.content

    print("\nRAW SUMMARY:")
    print(repr(summary))

    if summary is None:
        return None

    summary = summary.strip()

    if not summary:
        return None

    return summary
