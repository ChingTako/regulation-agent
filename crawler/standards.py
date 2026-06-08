import feedparser

QUERIES = [
    ("ISO", "https://news.google.com/rss/search?q=ISO+standard"),
    ("DIN", "https://news.google.com/rss/search?q=DIN+standard"),
    ("EN", "https://news.google.com/rss/search?q=EN+standard"),
    ("UL", "https://news.google.com/rss/search?q=UL+standard"),
    ("CNS", "https://news.google.com/rss/search?q=CNS+standard"),
    ("ASTM", "https://news.google.com/rss/search?q=ASTM+standard"),
    ("CSA", "https://news.google.com/rss/search?q=CSA+standard"),
    ("IEC", "https://news.google.com/rss/search?q=IEC+standard"),
    ("AS", "https://news.google.com/rss/search?q=AS+standard"),
]


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
            summary = entry.get("summary", "") or entry.get("description", "")

            results.append({
                "title": entry.title,
                "url": entry.link,
                "source": name,
                "summary": summary,
            })

    return results
