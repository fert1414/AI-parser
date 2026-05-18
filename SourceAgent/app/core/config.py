import os

from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass(frozen=True)
class Settings:
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