import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("Set BOT_TOKEN and CHAT_ID environment variables to actually send a message. Exiting.")
    exit(0)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": "測試成功 🚀"
}

r = requests.post(url, data=data)

print(r.text)