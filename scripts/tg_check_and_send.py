import os
import sys
import requests


def api_request(bot_token, method, params=None, post=False):
    url = f"https://api.telegram.org/bot{bot_token}/{method}"
    try:
        if post:
            r = requests.post(url, data=params or {})
        else:
            r = requests.get(url, params=params or {})
    except Exception as e:
        print(f"HTTP ERROR calling {method}: {e}")
        return None

    print(f"{method} -> {r.status_code} | {r.text}")
    return r


def main():
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not bot_token or not chat_id:
        print("ERROR: BOT_TOKEN and CHAT_ID must be set as environment variables.")
        sys.exit(1)

    # Check bot identity
    r = api_request(bot_token, "getMe")
    if not r or not r.ok:
        print("ERROR: getMe failed, check BOT_TOKEN.")
        sys.exit(2)

    bot_id = r.json().get("result", {}).get("id")
    print("Bot id:", bot_id)

    # If chat_id equals bot id, it's likely the wrong id
    try:
        # strip leading - for group ids when comparing
        if str(bot_id) == str(chat_id).lstrip("-"):
            print("ERROR: CHAT_ID equals the bot id. This is invalid — use your user id or the group's id instead.")
            sys.exit(3)
    except Exception:
        pass

    # Show updates (useful to find chat ids)
    api_request(bot_token, "getUpdates")

    # Try sending a test message
    text = "[regulation-agent] GitHub Actions test message"
    r2 = api_request(bot_token, "sendMessage", params={"chat_id": chat_id, "text": text}, post=True)
    if not r2 or not r2.ok:
        print("SEND FAILED")
        sys.exit(4)

    print("SEND OK")


if __name__ == "__main__":
    main()
