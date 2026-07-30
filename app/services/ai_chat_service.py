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

from app.utils.greetings import (
    GREETINGS,
    get_greeting_reply
)

from app.utils.small_talk import SMALL_TALK


def ai_chat(db, customer_id, message):

    # -------- Save User Message --------
    save_message(db, customer_id, "user", message)

    msg = message.lower().strip()

    # -------- FAST PATH: Greetings --------
    if msg in GREETINGS:
        reply = get_greeting_reply()
        save_message(db, customer_id, "assistant", reply)
        return reply

    # -------- FAST PATH: Small Talk --------
    for key, reply in SMALL_TALK.items():
        if key in msg:
            save_message(db, customer_id, "assistant", reply)
            return reply

    # -------- FAST PATH: Profile extraction (light check only) --------
    PROFILE_KEYWORDS = ["name", "budget", "phone", "location", "city", "contact"]

    if any(k in msg for k in PROFILE_KEYWORDS):
        try:
            profile_data = extract_profile(message)
            update_profile(db, customer_id, profile_data)
        except Exception as e:
            print("Profile extraction failed:", e)

    # -------- ONLY ONE DB CALL (IMPORTANT FIX) --------
    history = get_history(db, customer_id, limit=6)

    # -------- Summary (LIGHT ONLY - NO HEAVY PROCESS HERE) --------
    summary_record = get_summary(db, customer_id)
    summary_text = summary_record.summary if summary_record else ""

    # -------- Build Messages --------
    messages = []

    if summary_text:
        messages.append({
            "role": "system",
            "content": f"""
Conversation Summary:
{summary_text}
"""
        })

    for item in history:
        messages.append({
            "role": item.role,
            "content": item.message
        })

    # -------- AI RESPONSE (MAIN BOT SPEED DEPENDS HERE) --------
    reply = generate_reply(messages)

    save_message(db, customer_id, "assistant", reply)

    # -------- SUMMARY TRIGGER (IMPORTANT FIX) --------
    # ❌ DO NOT run heavy summary inside request
    # 👉 ONLY trigger flag here

    total_messages = len(history)

    if total_messages >= SUMMARY_TRIGGER:
        print("⚠️ Summary needed (should run in background worker)")

        # OPTIONAL: you can move this to background later
        try:
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