import os

from dotenv import load_dotenv
from dataclasses import dataclass

from backend.app.db.RDBMS_db.connection import get_postgres_db_connection

load_dotenv()

@dataclass(frozen=True)
class Settings:
    POSTGRES_DB_CONNECTION = get_postgres_db_connection()

    gigachat_api_url: str = os.getenv(
        "GIGACHAT_API_URL",
        "https://gigachat.devices.sberbank.ru/api/v1"
    )

    gigachat_api_key = os.getenv("GIGACHAT_API_KEY")

settings = Settings()