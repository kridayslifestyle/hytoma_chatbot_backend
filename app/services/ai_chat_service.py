from app.ai.profile_extractor import extract_profile
from app.services.profile_service import update_profile

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

        # -------- FAST PATH: Profile Extraction --------
        PROFILE_KEYWORDS = ["name", "budget", "phone", "location", "city", "contact"]

        if any(k in msg for k in PROFILE_KEYWORDS):
            try:
                profile_data = extract_profile(message)
                update_profile(db, customer_id, profile_data)
            except Exception as e:
                print("Profile extraction failed:", e)

        # -------- GET HISTORY (ONLY ONCE) --------
        history = get_history(db, customer_id, limit=6)

        # -------- GET SUMMARY (SAFE) --------
        summary_record = None
        summary_text = ""

        try:
            summary_record = get_summary(db, customer_id)
            if summary_record:
                summary_text = summary_record.summary
        except Exception as e:
            print("Summary fetch failed:", e)

        # -------- BUILD CONTEXT --------
        messages = []

        if summary_text:
            messages.append({
                "role": "system",
                "content": f"Conversation Summary:\n{summary_text}"
            })

        for item in history:
            messages.append({
                "role": item.role,
                "content": item.message
            })

        # -------- AI RESPONSE --------
        reply = generate_reply(messages)

        # -------- SAVE ASSISTANT RESPONSE --------
        save_message(db, customer_id, "assistant", reply)

        # -------- SUMMARY TRIGGER (NON-BLOCKING SAFE) --------
        try:
            total_messages = len(history)

            if total_messages >= SUMMARY_TRIGGER:

                print("⚠️ Summary triggered")

                full_history = get_history(db, customer_id, limit=100)

                summary_messages = [
                    {"role": item.role, "content": item.message}
                    for item in full_history
                ]

                summary = generate_summary(summary_messages)

                if summary:
                    save_summary(db, customer_id, summary)

        except Exception as e:
            print("Summary error:", e)

        return reply

    except Exception as e:
        print("AI CHAT ERROR:", e)
        db.rollback()
        return "Sorry, something went wrong. Please try again."