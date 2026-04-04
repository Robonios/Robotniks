"""
Robotnik Web Crawler
====================
Python-based web crawling utility for sources that don't have RSS feeds
or block standard urllib requests. Uses multiple strategies:

1. Direct fetch with browser-like headers
2. RSS feed discovery and parsing
3. Brave Search API as fallback for Cloudflare-protected sites

Usage:
  from web_crawler import WebCrawler
  crawler = WebCrawler()
  items = crawler.crawl_source("semi.org")

No external dependencies beyond stdlib + feedparser + beautifulsoup4
(already in requirements.txt).
"""

import json
import os
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

try:
    import feedparser
except ImportError:
    feedparser = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Load Brave API key from .env if available
BRAVE_API_KEY = os.environ.get('BRAVE_API_KEY', 'BSACkehe5LQN3p9USHE3AZAC8qU02G9')


class WebCrawler:
    """Multi-strategy web crawler for Robotnik data pipeline."""

    def __init__(self, cache_dir=None, rate_limit_seconds=2):
        self.cache_dir = cache_dir or os.path.join(ROOT_DIR, 'data', '.crawl_cache')
        self.rate_limit = rate_limit_seconds
        self._last_request = 0
        os.makedirs(self.cache_dir, exist_ok=True)

    def _throttle(self):
        """Respect rate limits between requests."""
        elapsed = time.time() - self._last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self._last_request = time.time()

    def fetch_url(self, url, headers=None):
        """Fetch a URL with browser-like headers. Returns (content, status) or (None, error)."""
        self._throttle()
        hdrs = dict(BROWSER_HEADERS)
        if headers:
            hdrs.update(headers)
        try:
            req = urllib.request.Request(url, headers=hdrs)
            resp = urllib.request.urlopen(req, timeout=15)
            return resp.read().decode('utf-8', errors='replace'), resp.status
        except Exception as e:
            return None, str(e)

    def fetch_rss(self, feed_url, max_items=30):
        """Fetch and parse an RSS feed. Returns list of item dicts."""
        if not feedparser:
            return []
        self._throttle()
        try:
            feed = feedparser.parse(feed_url)
            items = []
            for entry in feed.entries[:max_items]:
                title = (entry.get('title') or '').strip()
                link = (entry.get('link') or '').strip()
                if not title or not link:
                    continue
                # Parse date
                published = entry.get('published_parsed') or entry.get('updated_parsed')
                if published:
                    dt = datetime(*published[:6])
                    date_str = dt.strftime('%Y-%m-%d')
                else:
                    date_str = datetime.now().strftime('%Y-%m-%d')
                items.append({
                    'title': title,
                    'url': link,
                    'date': date_str,
                    'summary': (entry.get('summary') or '')[:500].strip(),
                })
            return items
        except Exception as e:
            print(f"    RSS fetch failed for {feed_url}: {e}")
            return []

    def brave_search(self, query, count=10):
        """Search using Brave Search API. Returns list of result dicts."""
        if not BRAVE_API_KEY:
            return []
        self._throttle()
        url = f"https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(query)}&count={count}"
        try:
            req = urllib.request.Request(url, headers={
                'Accept': 'application/json',
                'X-Subscription-Token': BRAVE_API_KEY,
            })
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode())
            results = data.get('web', {}).get('results', [])
            return [{
                'title': r.get('title', ''),
                'url': r.get('url', ''),
                'date': r.get('page_age', datetime.now().strftime('%Y-%m-%d')),
                'summary': r.get('description', ''),
            } for r in results]
        except Exception as e:
            print(f"    Brave Search failed: {e}")
            return []

    def scrape_html_links(self, url, link_selector=None, base_url=None):
        """Scrape article links from an HTML page using BeautifulSoup."""
        if not BeautifulSoup:
            return []
        content, status = self.fetch_url(url)
        if not content:
            return []
        soup = BeautifulSoup(content, 'lxml')
        items = []
        # Find article-like links
        for a in soup.find_all('a', href=True):
            href = a['href']
            title = a.get_text(strip=True)
            if not title or len(title) < 15:
                continue
            # Resolve relative URLs
            if href.startswith('/'):
                href = (base_url or url.rstrip('/')) + href
            if not href.startswith('http'):
                continue
            items.append({
                'title': title,
                'url': href,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'summary': '',
            })
        return items

    # ── Source-specific crawlers ────────────────────────────────────────

    def crawl_semi_org(self, months_back=3):
        """Crawl SEMI.org press releases via Brave Search (site is Cloudflare-protected)."""
        print("  [SEMI.org] Using Brave Search (site blocks direct access)")
        items = []
        queries = [
            f"site:semi.org press release {datetime.now().year}",
            f"site:semi.org semiconductor market report {datetime.now().year}",
        ]
        for q in queries:
            results = self.brave_search(q, count=10)
            items.extend(results)
            print(f"    Brave: '{q}' → {len(results)} results")

        # Deduplicate by URL
        seen = set()
        unique = []
        for item in items:
            if item['url'] not in seen:
                seen.add(item['url'])
                unique.append(item)
        print(f"  [SEMI.org] {len(unique)} unique items via Brave Search")
        return unique

    def crawl_space_foundation(self):
        """Crawl Space Foundation news via their RSS feed."""
        print("  [Space Foundation] Using RSS feed")
        items = self.fetch_rss("https://www.spacefoundation.org/feed/", max_items=30)
        # Filter to news/press items
        filtered = [i for i in items if 'spacefoundation.org' in i.get('url', '')]
        print(f"  [Space Foundation] {len(filtered)} items from RSS")
        return filtered

    def crawl_all_blocked_sources(self):
        """Crawl all sources that the standard RSS pipeline can't reach."""
        all_items = {}
        all_items['SEMI'] = self.crawl_semi_org()
        all_items['Space Foundation'] = self.crawl_space_foundation()
        return all_items


def main():
    """CLI entry point — crawl blocked sources and print results."""
    crawler = WebCrawler()
    print("Robotnik Web Crawler")
    print("=" * 50)

    results = crawler.crawl_all_blocked_sources()
    total = 0
    for source, items in results.items():
        total += len(items)
        print(f"\n{source}: {len(items)} items")
        for item in items[:3]:
            print(f"  {item['title'][:70]}")
            print(f"    {item['url']}")

    print(f"\nTotal: {total} items crawled")
    return results


if __name__ == '__main__':
    main()
