from crawler.fda import fetch_fda
from db.database import init_db, insert_regulation
from utils.filter import match
from notifier.telegram import send_telegram


def process(items):

    for item in items:

        title = item["title"]
        url = item["url"]
        source = item["source"]

        print("\n---")
        print("TITLE:", title)

        # 🔥 DEBUG 1：先看 match 結果
        is_match = match(title)
        print("MATCH RESULT:", is_match)

        # ⚠️ 暫時放寬：避免整個系統被 filter 卡死
        if not is_match:
            print("SKIP by match()")
            continue

        # 🔥 DEBUG 2：DB insert
        inserted = insert_regulation(title, url, source)
        print("INSERTED:", inserted)

        if not inserted:
            print("SKIP by DB (already exists or insert failed)")
            continue

        # 🚨 這裡才是 Telegram 發送點
        msg = f"""🚨 法規更新

📌 {title}
🏛 {source}
🔗 {url}
"""

        print("SENDING TELEGRAM...")

        send_telegram(msg)

        print("SENT:", title)


def run():

    init_db()

    print("Fetching FDA...")
    items = fetch_fda()

    print("Total:", len(items))

    # 🔥 如果你想「強制測試 Telegram」，取消下面這行註解
    # send_telegram("TEST MESSAGE - SYSTEM IS WORKING")

    process(items)


if __name__ == "__main__":
    run()