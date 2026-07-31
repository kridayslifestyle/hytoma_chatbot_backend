from app.ai.profile_extractor import extract_profile
from app.services.profile_service import update_profile
from app.rag.product_retriever import retrieve_products
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
from app.utils.helpers import is_price_query

def ai_chat(db, customer_id, message):

    try:
        # -------- Save User Message --------
        save_message(db, customer_id, "user", message)

        msg = message.lower().strip()

        # -------- FAST PATH: Greetings --------
        if msg in GREETINGS:
            reply = get_greeting_reply()
            save_message(db, customer_id, "assistant", reply)
            return reply

        # -------- FAST PATH: Small Talk --------
        for key, value in SMALL_TALK.items():
            if key in msg:
                save_message(db, customer_id, "assistant", value)
                return value

        # -------- FAST PATH: PROFILE --------
        PROFILE_KEYWORDS = ["name", "budget", "phone", "location", "city", "contact"]

        if any(k in msg for k in PROFILE_KEYWORDS):
            try:
                profile_data = extract_profile(message)
                update_profile(db, customer_id, profile_data)
            except Exception as e:
                print("Profile extraction failed:", e)

        # 🔥🔥🔥 ADD THIS BLOCK (VERY IMPORTANT)
        # -------- PRICE ROUTE (HIGHEST PRIORITY) --------
        if is_price_query(message):



            products = retrieve_products(message)

            if not products:
                reply = "Please contact Hytoma for best price & details 😊"
            else:
                reply = "\n".join([
                    f"- {p['name']}: ₹{p['price']}"
                    for p in products
                ]) + "\n\nFor best price contact us 😊"

            save_message(db, customer_id, "assistant", reply)
            return reply

    except Exception as e:
        print("AI CHAT ERROR:", e)
        db.rollback()
        return None