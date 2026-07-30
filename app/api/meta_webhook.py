from urllib import response

from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse
import json

from app.database.connection import SessionLocal

from app.services.ai_chat_service import ai_chat

from app.services.instagram_sender import send_instagram_message

from app.utils.typing import typing_delay

router = APIRouter()

VERIFY_TOKEN = "hytoma_verify_token"

BUSINESS_ACCOUNT_ID = "17841472803130955"


# ---------------- VERIFY WEBHOOK ----------------
@router.get("/webhook")
async def verify_webhook(request: Request):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge)

    return PlainTextResponse(content="Verification failed")


# ---------------- BACKGROUND WORKER ----------------
def process_message(sender_id: str, message_text: str, is_media=False):

    try:
        db = SessionLocal()

        # 1. MEDIA FLOW (FAST STATIC RESPONSE)
        if is_media:

            reply = (
                "Thank you for contacting Hytoma Automation LLP 😊\n\n"
                "Please share:\n"
                "- Name\n"
                "- Mobile\n"
                "- Location\n"
                "- Requirement"
            )

        else:

            # 2. AI CALL (ONLY THIS IS SLOW PART)
            reply = ai_chat(
                db=db,
                customer_id=sender_id,
                message=message_text
            )

        # 3. SEND MESSAGE (NON BLOCKING SAFE CALL)
        try:
            send_instagram_message(sender_id, reply)
        except Exception as e:
            print("Send message failed:", e)

    finally:
        db.close()



# ---------------- WEBHOOK ----------------
@router.post("/webhook")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):

    print("\n========== POST RECEIVED ==========")

    body = await request.json()

    print("\n========== FULL JSON ==========")
    print(json.dumps(body, indent=4))

    try:

        entry = body["entry"][0]

        sender_id = None
        message_text = None

        # -------- NEW FORMAT --------
        if "changes" in entry:

            value = entry["changes"][0]["value"]

            if "message" in value:

                sender_id = value["sender"]["id"]
                message_text = value["message"]["text"]

        # -------- OLD FORMAT --------
        elif "messaging" in entry:

            messaging = entry["messaging"][0]

            message = messaging.get("message", {})

            if message.get("attachments"):

                print("MEDIA RECEIVED")

                sender_id = messaging["sender"]["id"]

                background_tasks.add_task(
                    process_message,
                    sender_id,
                    None,
                    True  
                )
                return {"status": "media_processing"}
            

            if "message" in messaging:

                # Ignore echo messages (VERY IMPORTANT)
                if messaging["message"].get("is_echo"):
                    print("\nIgnoring echo message.")
                    return {"status": "ok"}

                sender_id = messaging["sender"]["id"]
                message_text = messaging["message"].get("text")

            elif "message_edit" in messaging:

                print("\nMessage edit event received.")
                return {"status": "ok"}

            else:

                print("\nIgnoring event.")
                return {"status": "ok"}

        else:

            print("\nUnknown payload structure.")
            return {"status": "ok"}

        if not sender_id or not message_text:

            print("\nNo message found.")
            return {"status": "ok"}

        print("\nSender ID:", sender_id)
        print("\nCustomer Message:", message_text)

        # Ignore business account messages
        if sender_id == BUSINESS_ACCOUNT_ID:
            print("\nIgnoring business account message.")
            return {"status": "ok"}

        # ---------------- INSTANT RESPONSE (NON-BLOCKING) ----------------
        background_tasks.add_task(
            process_message,
            sender_id,
            message_text,
            False
        )

        return {"status": "processing"}

    except Exception as e:
        print("\nERROR:", e)

    return {"status": "ok"}