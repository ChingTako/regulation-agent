import requests

BOT_TOKEN = "8958313466:AAE9tVCNlISwY6-3GsnyMFEiDvP35SENU4E"
CHAT_ID = "8546764711"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": "測試成功 🚀"
}

r = requests.post(url, data=data)

print(r.text)