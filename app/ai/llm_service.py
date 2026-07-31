from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- GROQ CLIENT ----------------
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- MAIN CHAT GENERATION ----------------
def generate_reply(messages):

    # keep token usage low (VERY IMPORTANT)
    response = client.chat.completions.create(
        model="llama3-8b-8192",

        messages=messages,

        temperature=0.3,
        max_tokens=250,   # 🔥 cost control

        top_p=1
    )

    reply = response.choices[0].message.content

    # safety cut (Instagram limit)
    if reply and len(reply) > 950:
        reply = reply[:950].rsplit(" ", 1)[0] + "..."

    return reply


# ---------------- SUMMARY (OPTIONAL BUT FREE) ----------------
def generate_summary(messages):

    conversation = ""

    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    response = client.chat.completions.create(
        model="llama3-8b-8192",

        messages=[
            {
                "role": "system",
                "content": "Summarize the conversation in under 80 words. Only facts."
            },
            {
                "role": "user",
                "content": conversation
            }
        ],

        temperature=0.2,
        max_tokens=120
    )

    summary = response.choices[0].message.content

    if not summary:
        return None

    return summary.strip()