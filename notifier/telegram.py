import os
import requests

def send_telegram(text, bot_token=None, chat_id=None):
    """Send a text message to Telegram using BOT_TOKEN and CHAT_ID from
    environment variables by default. Returns True on success.
    """

    bot_token = bot_token or os.getenv("BOT_TOKEN")
    chat_id = chat_id or os.getenv("CHAT_ID")

    if not bot_token or not chat_id:
        raise RuntimeError("BOT_TOKEN and CHAT_ID must be set in environment")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    r = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": text
        }
    )

    print("STATUS:", r.status_code)
    try:
        payload = r.json()
    except ValueError:
        payload = r.text
    print("RESPONSE:", payload)

    return r.ok