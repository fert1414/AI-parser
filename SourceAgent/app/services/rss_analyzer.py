import requests
import feedparser
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.core.logger import logger
from app.schemas.source_analyzer_schemas import Fields, FoundSource

class RSSAnalyzer:
    def __init__(self, AI_client, timeout = 15):
        self.timeout = timeout
        self.AI_client = AI_client
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

# ------------------------------------Functions fo search RSS------------------------------------

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
            
            if "alternate" in rel and ("rss" in type_ or "atom" in type_ or "xml" in type_):
                rss_feed = urljoin(str(source_link), href)

                response = requests.get(rss_feed, headers=self.headers, timeout=self.timeout)
                content_type = response.headers.get("Content-Type", "").lower()
                if "html" in content_type:
                    return None
                return rss_feed
            
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
                rss_feed = urljoin(str(source_link), href)

                response = requests.get(rss_feed, headers=self.headers, timeout=self.timeout)
                content_type = response.headers.get("Content-Type", "").lower()
                if "html" in content_type:
                    return None
                return rss_feed
        
        return None

    def _find_rss_by_llm(self, source_link: str) -> str | None:
        pass

# --------------------------------------Detection functions---------------------------------------

    def _get_feed_info(self, source_link, rss_feed) -> dict | None:
        found_source = FoundSource(source_link=source_link, fields=Fields())

        feed = feedparser.parse(rss_feed)

        if not feed:
            return found_source
        
        found_source.source_type = "feed"
        found_source.feed_link = rss_feed
        found_source.feed_format = feed.get("version", "")

        if feed.get("entries", []):
            first_entry = feed.entries[0]
            fields = Fields(
                title=bool(first_entry.get("title")),
                link=bool(first_entry.get("link")),
                summary=bool(first_entry.get("summary")),
                published=bool(first_entry.get("published"))
            )
            found_source.fields = fields

        return found_source

# -------------------------------------Main analyze function-------------------------------------

    def analyze_link(self, source_link: str) -> FoundSource:
        logger.info(f"Analyzing link for RSS feed: {source_link}")

        try:
            response = requests.get(source_link, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error(f"Failed to fetch source link {source_link}: {exc}")
            return FoundSource(source_link=source_link, fields=Fields())

        soup = BeautifulSoup(response.content, "html.parser")

        try:
            rss_feed = self._find_rss_in_meta(soup, source_link)
            if rss_feed:
                logger.info(f"Found RSS feed in meta tags: {rss_feed}")
                return self._get_feed_info(source_link, rss_feed)
            
            rss_feed = self._find_rss_in_anchor(soup, source_link)
            if rss_feed:
                logger.info(f"Found RSS feed in anchor tags: {rss_feed}")
                return self._get_feed_info(source_link, rss_feed)
            
        except Exception as exc:
            logger.error(f"Can't parse link for RSS: {exc}")

        return FoundSource(source_link=source_link, fields=Fields())