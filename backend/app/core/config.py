import os

from dotenv import load_dotenv
from dataclasses import dataclass

from app.db.RDBMS_db.connection import get_postgres_db_connection

load_dotenv()

@dataclass(frozen=True)
class Settings:
    POSTGRES_DB_CONNECTION = get_postgres_db_connection()

    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID")

    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    gigachat_api_url: str = os.getenv(
        "GIGACHAT_API_URL",
        "https://gigachat.devices.sberbank.ru/api/v1"
    )
    gigachat_api_key = os.getenv("GIGACHAT_API_KEY")

    openrouter_api_url: str = os.getenv(
        "OPENROUTER_API_URL",
        "https://openrouter.ai/api/v1"
    )
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY")

    yandexgpt_api_url: str = os.getenv(
        "YANDEXGPT_API_URL",
        "https://llm.api.cloud.yandex.net/foundationModels/v1"
    )
    yandexgpt_api_key: str = os.getenv("YANDEXGPT_API_KEY")
    yandexgpt_folder_id: str = os.getenv("YANDEXGPT_FOLDER_ID")

settings = Settings()