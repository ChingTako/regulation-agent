import feedparser
import urllib.parse
from datetime import datetime, timezone, timedelta
from utils.filter import match

URL = "https://www.fda.gov/about-fda/fda-newsroom/rss.xml"
FALLBACK_SEARCH_URL = "https://news.google.com/rss/search?q=" + urllib.parse.quote(
    'site:fda.gov ISO OR DIN OR UL OR ANSI OR RESNA OR EN OR JIS OR CNS OR AS OR NZS', safe=""
)


def _is_recent(entry, days=548):
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if not published:
        return True

    published_dt = datetime(*published[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - published_dt <= timedelta(days=days)


def fetch_fda():
    """Fetch FDA announcements from the official FDA Newsroom RSS feed."""

    feed = feedparser.parse(URL)
    if not getattr(feed, "entries", []):
        feed = feedparser.parse(FALLBACK_SEARCH_URL)

    results = []

    for entry in getattr(feed, "entries", []):
        if not _is_recent(entry, days=548):
            continue

        summary = entry.get("summary", "") or entry.get("description", "")
        text = f"{entry.title} {summary}"
        if not match(text):
            continue

        results.append({
            "title": entry.title,
            "url": entry.get("link"),
            "source": "FDA",
            "summary": summary,
        })

    return results