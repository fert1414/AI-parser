import requests
import feedparser
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.core.logger import logger
from app.core.exceptions import SourceAgentError

class RSSAnalyzer:
    def __init__(self, timeout = 15):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def _find_rss_in_meta(self, soup, source_link: str) -> str | None:
        for tag in soup.find_all("link"):
            rel = tag.get("rel", [])
            type_ = tag.get("type", "")
            href = tag.get("href", "")

            if not isinstance(href, str) or not href:
                continue
            if isinstance(rel, list):
                rel = " ".join(rel)

            rel = str(rel).lower()
            type_ = str(type_).lower()
            
            if "alternate" in rel and (
                "rss" in type_ or "atom" in type_ or "xml" in type_
            ):
                return urljoin(str(source_link), href)
            
        return None
    
    def _find_rss_in_anchor(self, soup, source_link: str) -> str | None:
        for tag in soup.find_all("a"):
            href = tag.get("href", "")
            text = tag.get_text(strip=True).lower()
            
            if not isinstance(href, str) or not href:
                continue
            href_lower = href.lower()

            href = tag.get("href", "")
            if (
                "rss" in text
                or "rss" in href_lower
                or href_lower.endswith(".rss")
                or href_lower.endswith(".xml")
                or "/feed" in href_lower
            ):
                return urljoin(str(source_link), href)
        
        return None

    def analyze_link(self, source_link: str) -> str | None:
        logger.info(f"Analyzing link for RSS feed: {source_link}")

        try:
            response = requests.get(source_link, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error(f"Failed to fetch source link {source_link}: {exc}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        try:
            rss_feed = self._find_rss_in_meta(soup, source_link)
            if rss_feed:
                logger.info(f"Found RSS feed in meta tags: {rss_feed}")
                return rss_feed
            
            rss_feed = self._find_rss_in_anchor(soup, source_link)
            if rss_feed:
                logger.info(f"Found RSS feed in anchor tags: {rss_feed}")
                return rss_feed
            
        except Exception as exc:
            logger.error(f"Can't parse link for RSS: {exc}")

        return None