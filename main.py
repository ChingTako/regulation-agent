import notifier.telegram as tg

print("TELEGRAM FILE PATH:", tg.__file__)
print("IMPORT:", tg.send_telegram)
from crawler.fda import fetch_fda
from crawler.standards import fetch_standards
from db.database import init_db, insert_regulation
from utils.filter import match


def process(items):
    new_count = 0
    duplicate_count = 0

    seen_urls = set()
    unique_items = []
    for item in items:
        url = item.get("url") or item.get("title")
        if url in seen_urls:
            duplicate_count += 1
            continue
        seen_urls.add(url)
        unique_items.append(item)

    candidate_count = len(unique_items)
    print(f"CANDIDATES FOUND: {candidate_count}, DUPLICATES SKIPPED: {duplicate_count}")

    for item in unique_items:
        title = item["title"]
        url = item["url"]
        source = item["source"]
        summary = item.get("summary", "") or ""

        print("\n---")
        print("TITLE:", title)
        print("SUMMARY:", summary[:120])

        # 🔥 DEBUG 1：先看 match 結果
        text = f"{title} {summary}"
        is_match = match(text)
        print("MATCH RESULT:", is_match)

        if not is_match:
            print("SKIP by match()")
            continue

        # 🔥 DEBUG 2：DB insert
        inserted = insert_regulation(title, url, source, summary)
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

        if summary:
            msg += f"\n📝 摘要：{summary}\n"

        print("SENDING TELEGRAM...")

        ok = tg.send_telegram(msg)

        if ok:
            print("SENT:", title)
            new_count += 1
        else:
            print("SEND FAILED:", title)

    print(f"SUMMARY: candidates={candidate_count}, sent={new_count}, duplicates={duplicate_count}")

    if candidate_count == 0:
        print("NO CANDIDATES, SENDING fallback message")
        tg.send_telegram("今天沒有新的規範")
    elif new_count == 0:
        print("FOUND candidates but no new alerts: all items already exist or insert failed")


def run():

    init_db()

    print("Fetching FDA...")
    items = fetch_fda()

    print("Fetching official standards sites (BSMI/CNS/ISO/IEC/ASTM/CEN/DIN/JIS/INTERTEK/ANSI)...")
    items += fetch_standards()

    print("Total:", len(items))

    # 🔥 如果你想「強制測試 Telegram」，取消下面這行註解
    # tg.send_telegram("TEST MESSAGE - SYSTEM IS WORKING")

    process(items)


if __name__ == "__main__":
    run()