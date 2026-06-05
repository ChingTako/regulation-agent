import requests

BOT_TOKEN = "8958313466:AAE9tVCNlISwY6-3GsnyMFEiDvP35SENU4E"
CHAT_ID = "8546764711"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

r = requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": "hello test"
})

print(r.status_code)
print(r.text)