import os
import requests

BOT_TOKEN = os.environ["8958313466:AAE9tVCNlISwY6-3GsnyMFEiDvP35SENU4E"]
CHAT_ID = os.environ["8546764711"]

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    r = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)