import feedparser

URL = "https://news.google.com/rss/search?q=FDA+medical+device"

def fetch_fda():

    feed = feedparser.parse(URL)

    results = []

    for entry in feed.entries:
        summary = entry.get("summary", "") or entry.get("description", "")

        results.append({
            "title": entry.title,
            "url": entry.link,
            "source": "FDA",
            "summary": summary
        })

    return results