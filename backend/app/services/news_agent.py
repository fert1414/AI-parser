from backend.app.core.logger import logger
from backend.app.services.news_extraction import NewsExtractor

class NewsAgent:
    def __init__(
        self, 
        postgres_db_connection,
        gigachat_client, 
        source_filters=None,
        theme_filters=None,
        news_update_interval=600
    ):
        self.postgres_db_connection = postgres_db_connection
        self.gigachat_client = gigachat_client
        self.source_filters = source_filters
        self.theme_filters = theme_filters
        self.news_update_interval = news_update_interval

    def run_news_extracting(self):
        logger.info("Running NewsAgent")

        news_extractor = NewsExtractor(self.postgres_db_connection, self.source_filters, self.news_update_interval)
        news = news_extractor.extract_news()
        return news