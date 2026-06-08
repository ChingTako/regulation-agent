import feedparser
import re
import requests
from datetime import datetime, timezone, timedelta

OFFICIAL_SOURCES = [
    {
        "name": "BSMI",
        "site": "bsmi.gov.tw",
        "homepage": "https://www.bsmi.gov.tw/",
        "rss": [],
    },
    {
        "name": "CNS",
        "site": "bsmi.gov.tw",
        "homepage": "https://www.bsmi.gov.tw/",
        "rss": [],
    },
    {
        "name": "ISO",
        "site": "iso.org",
        "homepage": "https://www.iso.org/news.html",
        "rss": [],
    },
    {
        "name": "IEC",
        "site": "iec.ch",
        "homepage": "https://www.iec.ch/news-events/news/",
        "rss": [],
    },
    {
        "name": "ASTM",
        "site": "astm.org",
        "homepage": "https://www.astm.org/news/",
        "rss": [],
    },
    {
        "name": "CEN/CENELEC",
        "site": "cencenelec.eu",
        "homepage": "https://www.cencenelec.eu/news/",
        "rss": [],
    },
    {
        "name": "DIN",
        "site": "din.de",
        "homepage": "https://www.din.de/en",
        "rss": [],
    },
    {
        "name": "JIS",
        "site": "jisc.go.jp",
        "homepage": "https://www.jisc.go.jp/en/",
        "rss": [],
    },
    {
        "name": "ANSI",
        "site": "ansi.org",
        "homepage": "https://www.ansi.org/news_publications/news",
        "rss": [],
    },
    {
        "name": "UL",
        "site": "ul.com",
        "homepage": "https://www.ul.com/news",
        "rss": [],
    },
    {
        "name": "RESNA",
        "site": "resna.org",
        "homepage": "https://www.resna.org/news",
        "rss": [],
    },
    {
        "name": "BSI",
        "site": "bsigroup.com",
        "homepage": "https://www.bsigroup.com/en-GB/about-bsi/media-centre/press-releases/",
        "rss": [],
    },
    {
        "name": "AS",
        "site": "standards.org.au",
        "homepage": "https://www.standards.org.au/news",
        "rss": ["https://www.standards.org.au/news/rss.xml"],
    },
    {
        "name": "NZS",
        "site": "standards.govt.nz",
        "homepage": "https://www.standards.govt.nz/",
        "rss": [],
    },
    {
        "name": "INTERTEK",
        "site": "intertek.com",
        "homepage": "https://www.intertek.com/news/",
        "rss": [],
    },
    {
        "name": "INTERTEK INFORM",
        "site": "intertekinform.com",
        "homepage": "https://www.intertekinform.com/",
        "rss": [],
    },
]

GOOGLE_SEARCH_TEMPLATE = "https://news.google.com/rss/search?q=site:{site}"
REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0"}


def _is_recent(entry, days=1):
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if not published:
        return True

    published_dt = datetime(*published[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - published_dt <= timedelta(days=days)


def _discover_rss_links(page_url):
    try:
        r = requests.get(page_url, headers=REQUEST_HEADERS, timeout=10)
        if r.status_code != 200:
            return []

        text = r.text
        links = re.findall(r'<link[^>]+type=["\'](?:application/rss\+xml|application/atom\+xml)["\'][^>]*>', text, re.IGNORECASE)
        rss_urls = []
        for link in links:
            hrefs = re.findall(r'href=["\']([^"\']+)["\']', link, re.IGNORECASE)
            if hrefs:
                rss_urls.append(hrefs[0])

        return [u if u.startswith("http") else requests.compat.urljoin(page_url, u) for u in rss_urls]
    except requests.RequestException:
        return []


def _parse_feed(feed_url):
    feed = feedparser.parse(feed_url)
    return getattr(feed, "entries", []) or []


def _fetch_official_source(source):
    rss_urls = list(source.get("rss", []))
    if not rss_urls:
        rss_urls = _discover_rss_links(source["homepage"])

    results = []
    for rss_url in rss_urls:
        for entry in _parse_feed(rss_url):
            if not _is_recent(entry, days=548):
                continue

            summary = entry.get("summary", "") or entry.get("description", "")
            results.append({
                "title": entry.title,
                "url": entry.link,
                "source": source["name"],
                "summary": summary,
            })

    return results


def _fetch_search_source(source):
    search_url = GOOGLE_SEARCH_TEMPLATE.format(site=source["site"])
    feed = feedparser.parse(search_url)
    results = []

    for entry in getattr(feed, "entries", []):
        if not _is_recent(entry, days=548):
            continue

        summary = entry.get("summary", "") or entry.get("description", "")
        results.append({
            "title": entry.title,
            "url": source["homepage"],
            "source": source["name"],
            "summary": summary,
        })

    return results


def fetch_standards():
    """Fetch recent news items from official standards organization domains."""

    results = []
    for source in OFFICIAL_SOURCES:
        official_results = _fetch_official_source(source)
        if official_results:
            results.extend(official_results)
            continue

        results.extend(_fetch_search_source(source))

    return results
