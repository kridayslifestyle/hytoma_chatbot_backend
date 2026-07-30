import os
import requests
from dotenv import load_dotenv

load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")


def send_instagram_message(recipient_id, text):

    # -----------------------------
    # LIMIT MESSAGE SIZE (IMPORTANT)
    # -----------------------------
    if not text:
        return None

    if len(text) > 950:
        text = text[:950].rsplit(" ", 1)[0] + "..."

    url = "https://graph.instagram.com/v25.0/me/messages"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text
        }
    }

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            params=params,
            json=payload,
            timeout=30
        )

        print("\n========== SEND MESSAGE ==========")
        print(response.status_code)

        try:
            print(response.json())
        except Exception:
            print(response.text)

        # -----------------------------
        # CHECK FAILURE
        # -----------------------------
        if response.status_code != 200:
            print("\n❌ Instagram API Error")
            print(response.text)

        # 🔥 IMPORTANT FIX
        return response

    except Exception as e:
        print("\n❌ REQUEST FAILED:")
        print(e)

        return None