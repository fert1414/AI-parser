from backend.app.core.config import settings
from backend.app.core.logger import logger

from backend.app.clients.gigachat_client import GigaChatClient
from backend.app.clients.openrouter_client import OpenRouterClient
from backend.app.clients.yandexgpt_api import YandexGPTClient
from backend.app.services.news_agent import NewsAgent

def main():
    logger.info("Starting the system...")

    source_filters = [
        "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"
    ]
    theme_filters = {
        "keywords": ["спорт", "олимпиада", "чемпионат"],
        "exclude_keywords": ["спорт", "культура"]
    }

    gigachat_client = GigaChatClient(settings.gigachat_api_url, settings.gigachat_api_key)
    openrouter_client = OpenRouterClient(settings.openrouter_api_url, settings.openrouter_api_key)
    yandexgpt_client = YandexGPTClient(settings.yandexgpt_api_url, settings.yandexgpt_api_key, settings.yandexgpt_folder_id)

    news_agent = NewsAgent(settings.POSTGRES_DB_CONNECTION, yandexgpt_client, source_filters, theme_filters, 3600)
    news = news_agent.run_news_extracting()
    print(news, len(news))

if __name__ == "__main__":
    main()