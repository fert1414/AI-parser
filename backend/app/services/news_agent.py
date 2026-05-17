from backend.app.core.logger import logger

from backend.app.services.news_filter import NewsFilter
from backend.app.services.news_extraction import NewsExtractor

class NewsAgent:
    def __init__(
        self, 
        postgres_db_connection,
        AI_client, 
        source_filters=None,
        theme_filters=None,
        news_update_interval=600
    ):
        self.postgres_db_connection = postgres_db_connection
        self.AI_client = AI_client
        self.source_filters = source_filters
        self.theme_filters = theme_filters
        self.news_update_interval = news_update_interval

    def run_news_extracting(self):
        logger.info("Running NewsAgent")

        news_extractor = NewsExtractor(self.postgres_db_connection, self.source_filters, self.news_update_interval)
        news = news_extractor.extract_news()

        news_filter = NewsFilter(self.AI_client)
        news = news_filter.filter_news(news, self.theme_filters)

        return news
