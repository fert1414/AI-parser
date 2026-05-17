import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

from app.core.logger import logger

load_dotenv()

class QdrantDBConnection:
    def __init__(self):
        self.client = QdrantClient(
            host=os.getenv("QDRANT_DB_HOST"),
            port=os.getenv("QDRANT_DB_PORT")
        )

def get_qdrant_db_connection():
    try:
        qdrant_db_connection = QdrantDBConnection()
    except Exception as exc:
        logger.error(f"Failed to create Qdrant database connection: {exc}")
        raise Exception(f"Failed to create Qdrant database connection: {exc}")
    return qdrant_db_connection