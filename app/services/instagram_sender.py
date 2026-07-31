import os
import requests
from dotenv import load_dotenv

load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")


# ---------------- SPLIT MESSAGE SAFELY ----------------
def split_message(text, limit=900):
    if not text:
        return []

    lines = text.split("\n")
    chunks = []
    current = ""

    for line in lines:
        if len(current) + len(line) + 1 > limit:
            chunks.append(current)
            current = line
        else:
            current += "\n" + line if current else line

    if current:
        chunks.append(current)

    return chunks


# ---------------- SEND MESSAGE ----------------
def send_instagram_message(recipient_id, text):

    if not text:
        return None

    url = "https://graph.facebook.com/v19.0/me/messages"

    headers = {
        "Content-Type": "application/json"
    }

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    messages = split_message(text)

    responses = []

    try:
        for msg in messages:

            payload = {
                "recipient": {
                    "id": recipient_id
                },
                "message": {
                    "text": msg
                }
            }

            response = requests.post(
                url,
                headers=headers,
                params=params,
                json=payload,
                timeout=10
            )

            print("\n========== SEND MESSAGE ==========")
            print(response.status_code)

            try:
                print(response.json())
            except Exception:
                print(response.text)

            if response.status_code != 200:
                print("\n❌ Instagram API Error")
                print(response.text)

            responses.append(response)

        return responses

    except Exception as e:
        print("\n❌ REQUEST FAILED:")
        print(e)
        return None