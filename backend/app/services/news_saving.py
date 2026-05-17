from app.core.logger import logger

class NewsSaver:
    def __init__(self, postgres_db_connection):
        self.postgres_db_connection = postgres_db_connection

    def save_news(self, news):
        # Implement the logic to save news to the database
        pass