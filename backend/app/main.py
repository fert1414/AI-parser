from backend.app.core.config import settings
from backend.app.core.logger import logger

from backend.app.clients.gigachat_client import GigachatClient
from backend.app.services.news_agent import NewsAgent

def main():
    logger.info("Starting the system...")

    source_filters = [
        "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"
    ]
    theme_filters = {
        "keywords": ["экономика", "финансы", "рынок"],
        "exclude_keywords": ["спорт", "культура"]
    }

    gigachat_client = GigachatClient(settings.gigachat_api_url, settings.gigachat_api_key)

    news_agent = NewsAgent(settings.POSTGRES_DB_CONNECTION, gigachat_client, source_filters, theme_filters)
    news = news_agent.run_news_extracting()
    print(news[0], len(news))

if __name__ == "__main__":
    main()