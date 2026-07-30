"""
Application-wide constants
"""

# -----------------------------
# Conversation Memory
# -----------------------------

# Number of recent messages to send to the LLM
MAX_HISTORY = 20

# Generate a conversation summary after every N messages
SUMMARY_TRIGGER = 100


# -----------------------------
# AI Models
# -----------------------------

DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324"


# -----------------------------
# Summary Prompt
# -----------------------------

SUMMARY_SYSTEM_PROMPT = """
Summarize the conversation.

Preserve:

- Customer interests
- Products discussed
- Decisions made
- Preferences
- Important details

Keep the summary short and concise.
"""


# -----------------------------
# Main System Prompt
# -----------------------------

SYSTEM_PROMPT = """
You are Hytoma AI.

You are a professional customer support assistant.

Your responsibilities:

- Answer customer questions accurately.
- Be polite and professional.
- Keep replies concise.
- If information is unavailable, clearly say so.
- Never invent product specifications or prices.
- Help customers with product information and support.
"""