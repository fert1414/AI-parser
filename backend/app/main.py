from apscheduler.schedulers.blocking import BlockingScheduler

from app.core.config import settings
from app.core.logger import logger

from app.clients.gigachat_client import GigaChatClient
from app.clients.openrouter_client import OpenRouterClient
from app.clients.yandexgpt_api import YandexGPTClient
from app.services.news_agent import NewsAgent

logger.info("Starting the system...")

source_filters = [
    "https://rssexport.rbc.ru/rbcnews/news/30/full.rss"
]

theme_filters = {
    "keywords": ["спорт", "олимпиада", "чемпионат"],
    "exclude_keywords": ["культура"]
}

gigachat_client = GigaChatClient(
    settings.gigachat_api_url,
    settings.gigachat_api_key
)

openrouter_client = OpenRouterClient(
    settings.openrouter_api_url,
    settings.openrouter_api_key
)

yandexgpt_client = YandexGPTClient(
    settings.yandexgpt_api_url,
    settings.yandexgpt_api_key,
    settings.yandexgpt_folder_id
)

news_agent = NewsAgent(
    settings.POSTGRES_DB_CONNECTION,
    yandexgpt_client,
    settings.TELEGRAM_BOT_TOKEN,
    settings.TELEGRAM_CHAT_ID,
    source_filters,
    theme_filters
)


def job():
    logger.info("Starting parsing...")
    
    try:
        news_agent.run_news_extracting()
        logger.info("Parsing finished")

    except Exception as e:
        logger.exception(f"Parsing error: {e}")


scheduler = BlockingScheduler()

scheduler.add_job(
    job,
    trigger="interval",
    minutes=10
)


if __name__ == "__main__":
    logger.info("Scheduler started")

    job()

    scheduler.start()
