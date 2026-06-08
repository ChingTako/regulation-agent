import feedparser
import re
import requests
import urllib.parse
from datetime import datetime, timezone, timedelta
from utils.filter import match, STANDARD_PATTERNS

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

GOOGLE_SEARCH_TEMPLATE = "https://news.google.com/rss/search?q={query}"
REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0"}

SEARCH_KEYWORDS_BY_SOURCE = {
    "BSMI": ["CNS", "AS NZS", "AS", "NZS"],
    "CNS": ["CNS", "AS NZS", "AS", "NZS"],
    "ISO": ["ISO", "EN"],
    "IEC": ["IEC", "ISO", "EN"],
    "ASTM": ["ASTM"],
    "CEN/CENELEC": ["EN", "BS EN"],
    "DIN": ["DIN"],
    "JIS": ["JIS"],
    "ANSI": ["ANSI", "UL"],
    "UL": ["UL"],
    "RESNA": ["RESNA", "WC-1"],
    "BSI": ["BS EN", "ISO", "EN"],
    "AS": ["AS NZS", "AS", "NZS"],
    "NZS": ["AS NZS", "AS", "NZS"],
    "INTERTEK": ["ISO", "DIN", "UL", "ANSI", "RESNA", "EN", "JIS", "CNS", "AS"],
    "INTERTEK INFORM": ["ISO", "DIN", "UL", "ANSI", "RESNA", "EN", "JIS", "CNS", "AS"],
}


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
            text = f"{entry.title} {summary}"
            if not match(text):
                continue
            results.append({
                "title": entry.title,
                "url": entry.link,
                "source": source["name"],
                "summary": summary,
            })

    return results


def _get_search_patterns(source):
    name = source["name"]
    if name in ("INTERTEK", "INTERTEK INFORM"):
        return []
    if name in ("BSMI", "CNS"):
        return [p for p in STANDARD_PATTERNS if p.startswith("CNS") or p.startswith("AS NZS") or p.startswith("AS ") or p.startswith("NZS ")]
    if name == "ISO":
        return [p for p in STANDARD_PATTERNS if "ISO" in p or p.startswith("EN ") or p.startswith("BS EN ") or p.startswith("DS EN ")]
    if name == "IEC":
        return [p for p in STANDARD_PATTERNS if "IEC" in p or "ISO" in p or p.startswith("EN ") or p.startswith("BS EN ")]
    if name == "CEN/CENELEC":
        return [p for p in STANDARD_PATTERNS if p.startswith("EN ") or p.startswith("BS EN ") or p.startswith("DS EN ")]
    if name == "DIN":
        return [p for p in STANDARD_PATTERNS if p.startswith("DIN ")]
    if name == "JIS":
        return [p for p in STANDARD_PATTERNS if p.startswith("JIS ")]
    if name == "ANSI":
        return [p for p in STANDARD_PATTERNS if p.startswith("ANSI ")]
    if name == "UL":
        return [p for p in STANDARD_PATTERNS if p.startswith("UL ") or p.startswith("ANSI CAN UL ")]
    if name == "RESNA":
        return [p for p in STANDARD_PATTERNS if "RESNA" in p or "WC-1" in p]
    if name == "BSI":
        return [p for p in STANDARD_PATTERNS if p.startswith("BS EN ") or p.startswith("BS EN ISO ")]
    if name in ("AS", "NZS"):
        return [p for p in STANDARD_PATTERNS if p.startswith("AS ") or p.startswith("NZS ") or p.startswith("AS NZS")]
    return []


def _build_search_query(source):
    patterns = _get_search_patterns(source)
    if patterns:
        quoted_terms = [f'"{term}"' if " " in term or "-" in term else term for term in patterns]
        return f"site:{source['site']} " + " OR ".join(quoted_terms)

    keywords = SEARCH_KEYWORDS_BY_SOURCE.get(source["name"], [])
    if not keywords:
        return f"site:{source['site']}"

    quoted_terms = []
    for term in keywords:
        if " " in term or "-" in term:
            quoted_terms.append(f'"{term}"')
        else:
            quoted_terms.append(term)

    return f"site:{source['site']} " + " OR ".join(quoted_terms)


def _build_search_url(source):
    query = _build_search_query(source)
    encoded = urllib.parse.quote(query, safe="")
    return GOOGLE_SEARCH_TEMPLATE.format(query=encoded)


def _fetch_search_source(source):
    search_url = _build_search_url(source)
    feed = feedparser.parse(search_url)
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
            "url": entry.get("link") or source["homepage"],
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
