from app.ai.profile_extractor import extract_profile
from app.services.profile_service import update_profile
from app.rag.product_retriever import retrieve_products
from app.rag.retriever import retrieve_context
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.services.chat_service import (
    save_message,
    get_history
)

from app.ai.llm_service import (
    generate_reply,
    generate_summary
)

from app.services.summary_service import (
    get_summary,
    save_summary
)

from app.utils.constants import SUMMARY_TRIGGER
from app.utils.greetings import GREETINGS, get_greeting_reply
from app.utils.small_talk import SMALL_TALK
from app.utils.helpers import is_price_query, is_product_query

def ai_chat(db, customer_id, message):

    try:
        save_message(db, customer_id, "user", message)

        msg = message.lower().strip()

        # ---------------- GREETING ----------------
        if msg in GREETINGS:
            reply = get_greeting_reply()
            save_message(db, customer_id, "assistant", reply)
            return reply

        # ---------------- SMALL TALK ----------------
        for key, value in SMALL_TALK.items():
            if key in msg:
                save_message(db, customer_id, "assistant", value)
                return value

        # ---------------- PROFILE ----------------
        PROFILE_KEYWORDS = ["name", "budget", "phone", "location", "city", "contact"]

        if any(k in message.lower() for k in PROFILE_KEYWORDS):
            try:
                profile_data = extract_profile(message)
                update_profile(db, customer_id, profile_data)
            except Exception as e:
                print("Profile error:", e)

        # ---------------- PRICE ROUTE ----------------
        if is_price_query(msg) or is_product_query(msg):
            

            products = retrieve_products(message)

            if not products:
                reply = "Please contact Hytoma for best price & details 😊"
            else:
                reply = "\n".join(
                    [f"- {p['name']}: ₹{p['price']}" for p in products]
                ) + "\n\nFor best price contact us 😊"

            save_message(db, customer_id, "assistant", reply)
            return reply

        # ---------------- HISTORY (SAFE) ----------------
        try:
            history = get_history(db, customer_id, limit=6)
        except Exception as e:
            print("History error:", e)
            history = []

        # ---------------- SUMMARY (SAFE) ----------------
        summary_text = ""
        try:
            summary_record = get_summary(db, customer_id)
            if summary_record:
                summary_text = summary_record.summary
        except Exception as e:
            print("Summary error:", e)

        # ---------------- RAG CONTEXT (SAFE) ----------------
        context_text = ""
        try:
            context_text = retrieve_context(message)
        except Exception as e:
            print("RAG retrieval error:", e)
            context_text = ""

        # ---------------- BUILD MESSAGES ----------------
        messages = []

        # Real system prompt, with retrieved document context injected
        messages.append({
            "role": "system",
            "content": SYSTEM_PROMPT.format(
                context=context_text or "No extra context available."
            )
        })

        if summary_text:
            messages.append({
                "role": "system",
                "content": f"Conversation Summary:\n{summary_text}"
            })

        for item in history:
            messages.append({
                "role": item.role,
                "content": item.message[:200]
            })

        # ---------------- LLM CALL ----------------
        reply = generate_reply(messages)

        save_message(db, customer_id, "assistant", reply)

        return reply

    except Exception as e:
        print("AI CHAT ERROR:", e)
        db.rollback()

        # 🔥 IMPORTANT FALLBACK (NEVER FAIL SILENTLY)
        return "Sorry, something went wrong. Please try again 😊"