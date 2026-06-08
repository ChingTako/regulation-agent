import feedparser
from datetime import datetime, timezone, timedelta

QUERIES = [
    ("BSMI", "https://news.google.com/rss/search?q=site:bsmi.gov.tw"),
    ("CNS", "https://news.google.com/rss/search?q=site:cnsonline.com.tw"),
    ("ISO", "https://news.google.com/rss/search?q=site:iso.org"),
    ("IEC", "https://news.google.com/rss/search?q=site:iec.ch"),
    ("ASTM", "https://news.google.com/rss/search?q=site:astm.org"),
    ("CEN", "https://news.google.com/rss/search?q=site:cencenelec.eu"),
    ("DIN", "https://news.google.com/rss/search?q=site:din.de"),
    ("JIS", "https://news.google.com/rss/search?q=site:jisc.go.jp"),
    ("INTERTEK", "https://news.google.com/rss/search?q=site:intertekinform.com"),
    ("ANSI", "https://news.google.com/rss/search?q=site:ansi.org"),
]


def _is_recent(entry, days=7):
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if not published:
        return True

    published_dt = datetime(*published[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - published_dt <= timedelta(days=days)



def fetch_standards():
    """Fetch recent news items related to common standards organizations.

    This uses Google News RSS search as a lightweight source of new articles
    mentioning the standards. Each entry includes title, link, source and
    summary (if available).
    """

    results = []

    for name, url in QUERIES:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            if not _is_recent(entry, days=7):
                continue

            summary = entry.get("summary", "") or entry.get("description", "")

            results.append({
                "title": entry.title,
                "url": entry.link,
                "source": name,
                "summary": summary,
            })

    return results
