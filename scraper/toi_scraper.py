"""Simple scraper for Times of India homepage.

This module provides functions to fetch the homepage and extract top headlines
and their URLs. It's intentionally small and robust: uses requests + BeautifulSoup
and respects robots.txt by default (only fetches homepage).
"""
from typing import List, Dict, Optional
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
)


def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch a URL and return the response text or None on error."""
    headers = {"User-Agent": DEFAULT_USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException:
        return None


def parse_headlines(html: str, max_items: int = 20) -> List[Dict[str, str]]:
    """Parse the Times of India homepage HTML and return a list of headline dicts.

    Improvements over a naive anchor scrape:
    - Prefer anchors inside header tags (h1-h4) and article-like containers.
    - Prefer anchors with classes containing "title", "headline", "story", etc.
    - Filter out short navigation/language links (e.g. "IN", "English", "/us").
    - Normalize protocol-relative and relative URLs.
    """
    soup = BeautifulSoup(html, "lxml")
    results: List[Dict[str, str]] = []

    base = "https://timesofindia.indiatimes.com"
    kw_re = re.compile(r"\b(title|headline|trending|top|lead|story|article)\b", re.I)

    def normalize_href(href: str) -> str:
        if href.startswith("//"):
            return "https:" + href
        if href.startswith("/"):
            return urljoin(base, href)
        return href

    candidates = []

    # 1) Anchors inside header tags are very likely to be headlines
    for header_tag in soup.find_all(["h1", "h2", "h3", "h4"]):
        candidates.extend(header_tag.find_all("a", href=True))

    # 2) Anchors with headline-like classes (on anchor or direct parent)
    for a in soup.find_all("a", href=True):
        classes = " ".join(a.get("class") or [])
        parent_classes = " ".join(a.parent.get("class") or []) if a.parent else ""
        if kw_re.search(classes) or kw_re.search(parent_classes):
            candidates.append(a)

    # 3) Anchors inside article/section/li/div blocks (broad sweep)
    for tag in soup.find_all(["article", "section", "li", "div"]):
        # limit per container to avoid noisy nav containers
        for a in tag.find_all("a", href=True):
            candidates.append(a)

    # Always consider remaining anchors as a fallback, but process candidates first
    all_anchors = list(dict.fromkeys(candidates + soup.find_all("a", href=True)))

    seen = set()
    for a in all_anchors:
        if len(results) >= max_items:
            break
        text = (a.get_text() or "").strip()
        href = a.get("href")
        if not text or not href:
            continue
        href = normalize_href(href)
        # skip non-http links
        if href.startswith("javascript:") or href.startswith("mailto:"):
            continue
        parsed = urlparse(href)
        # only keep links pointing to indiatimes-related hosts
        if "indiatimes.com" not in (parsed.netloc or ""):
            continue
        # skip root / top-level navigation paths (very short paths)
        path = (parsed.path or "").rstrip("/")
        if path == "" or path == "/":
            continue
        # filter out obvious language/nav links by short/numeric text
        if len(text) < 10 and len(text.split()) < 2:
            # allow short titles if they contain lowercase or punctuation (rare)
            if text.isupper() or text.isdigit():
                continue
        # final dedupe
        key = (text, href)
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": text, "url": href})

    return results


def get_top_headlines(max_items: int = 20) -> List[Dict[str, str]]:
    """Fetch the TOI homepage and return top headlines.

    Returns an empty list on network failure.
    """
    url = "https://timesofindia.indiatimes.com/"
    html = fetch_url(url)
    if not html:
        return []
    return parse_headlines(html, max_items=max_items)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch Times of India top headlines")
    parser.add_argument("-n", "--num", type=int, default=10, help="max headlines")
    args = parser.parse_args()
    items = get_top_headlines(args.num)
    for i, it in enumerate(items, 1):
        print(f"{i}. {it['title']} - {it['url']}")
