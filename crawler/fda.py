import feedparser
from datetime import datetime, timezone, timedelta

URL = "https://www.fda.gov/about-fda/fda-newsroom/rss.xml"


def _is_recent(entry, days=180):
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if not published:
        return True

    published_dt = datetime(*published[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - published_dt <= timedelta(days=days)


def fetch_fda():
    """Fetch FDA announcements from the official FDA Newsroom RSS feed."""

    feed = feedparser.parse(URL)
    results = []

    for entry in feed.entries:
        if not _is_recent(entry, days=7):
            continue

        summary = entry.get("summary", "") or entry.get("description", "")

        results.append({
            "title": entry.title,
            "url": entry.link,
            "source": "FDA",
            "summary": summary
        })

    return results
    return results