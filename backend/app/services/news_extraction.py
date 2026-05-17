import feedparser
from dateutil import parser
from datetime import datetime, UTC

from app.core.logger import logger

from app.db.RDBMS_db.repositories.news_sources import NewsSourceRepository

class NewsExtractor:
    def __init__(
        self, 
        postgres_db_connection, 
        source_filters=None,
        news_update_interval=600
    ):
        self.postgres_db_connection = postgres_db_connection
        self.source_filters = source_filters
        self.news_update_interval = news_update_interval
        self.news_source_repository = NewsSourceRepository(postgres_db_connection)

        self.current_time = datetime.now(UTC)

    def _extract_news_sources(self):
        return self.news_source_repository.get_news_sources(self.source_filters)

    def _extract_from_rss(self, source):
        logger.info(f"Extracting news from RSS feed: {source['url']}")

        feed = feedparser.parse(source["url"])

        news = []

        for item in feed.entries:
            published = item.get("published", "")
            if published:
                published = parser.parse(published)

            if (self.current_time - published).total_seconds() > self.news_update_interval:
                continue

            news_item = {
                "source_id": source["id"],
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "published": published,
                "summary": item.get("summary", "")
            }
            news.append(news_item)

        return news

    def extract_news(self):
        logger.info("Extracting news sources...")
        news_sources = self._extract_news_sources()
        news = []

        logger.info("Extracting news...")
        for source in news_sources:
            logger.info(f"Extracting news from source: {source['name']} (ID: {source['id']})")
            
            if source["fetch_method"] == "rss":
                news.extend(self._extract_from_rss(source))

        return news