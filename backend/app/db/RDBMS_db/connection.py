import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

from app.core.logger import logger
from app.core.exceptions import RDBMSConnectionError

load_dotenv()

class PostgresDBConnection:
    def __init__(self):
        self.connection = psycopg.connect(
            host=os.getenv("POSTGRES_DB_HOST"),
            port=os.getenv("POSTGRES_DB_PORT"),
            dbname=os.getenv("POSTGRES_DB_NAME"),
            user=os.getenv("POSTGRES_DB_USER"),
            password=os.getenv("POSTGRES_DB_PASSWORD"),
            row_factory=dict_row
        )

def get_postgres_db_connection():
    try:
        postgres_db_connection = PostgresDBConnection()
    except Exception as exc:
        logger.error(f"Failed to create PostgreSQL database connection: {exc}")
        raise RDBMSConnectionError(f"Failed to create PostgreSQL database connection: {exc}")
    return postgres_db_connection