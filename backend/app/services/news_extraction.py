from unittest import result

import feedparser
from ddgs import DDGS
from dateutil import parser
from datetime import datetime, UTC

from app.core.logger import logger

from app.db.RDBMS_db.repositories.news_sources import NewsSourceRepository
from app.prompts.source_propts import create_source_finder_prompt

from app.core.config import settings

class NewsExtractor:
    def __init__(
        self, 
        postgres_db_connection,
        AI_client, 
        source_filters=None,
        news_update_interval=600
    ):
        self.postgres_db_connection = postgres_db_connection
        self.AI_client = AI_client
        self.source_filters = source_filters
        self.news_update_interval = news_update_interval
        self.news_source_repository = NewsSourceRepository(postgres_db_connection)

        self.current_time = datetime.now(UTC)

    def _extract_news_sources(self):
        found_sources = self.news_source_repository.get_news_sources(self.source_filters)

        for source in self.source_filters:
            if not any(found_source["method_url"] == source for found_source in found_sources):
                # source_finder_prompt = create_source_finder_prompt(source)
                # result = self.AI_client.ask_json(source_finder_prompt)

                queries = [
                    f"{source} RSS",
                    f"{source} feed",
                    f'"{source}" "rss"',
                    f'"{source}" "atom"',
                ]
                
                urls = []
                for query in queries:
                    with DDGS() as ddgs:
                        results = ddgs.text(
                            query,
                            max_results=10,
                            # backend="google"
                        )

                    urls.extend([item["href"] for item in results if item["href"]])

                results = []
                for url in urls:
                    source_finder_prompt = create_source_finder_prompt(url)
                    result = self.AI_client.ask_json(source_finder_prompt)
                    print(result)
                    results.append(result)

                logger.info(f"Source {source} not found in database")
                logger.info(f"AI response for source: {results}")
                continue

        return found_sources

    def _extract_from_rss(self, source):
        logger.info(f"Extracting news from RSS feed: {source['method_url']}")

        feed = feedparser.parse(source["method_url"])

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