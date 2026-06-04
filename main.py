from crawler.fda import fetch_fda
from db.database import init_db, insert_regulation
from utils.filter import match
from notifier.telegram import send_telegram


def process(items):

    for item in items:

        title = item["title"]
        url = item["url"]
        source = item["source"]

        if match(title):

            inserted = insert_regulation(title, url, source)

            if inserted:

                msg = f"""🚨 法規更新

📌 {title}
🏛 {source}
🔗 {url}
"""

                send_telegram(msg)
                print("SENT:", title)


def run():

    init_db()

    print("Fetching FDA...")
    items = fetch_fda()

    print("Total:", len(items))

    process(items)


if __name__ == "__main__":
    run()