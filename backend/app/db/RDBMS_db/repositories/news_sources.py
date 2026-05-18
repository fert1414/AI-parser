from app.core.exceptions import RDBMSQueryError
from app.core.logger import logger

class NewsSourceRepository:
    def __init__(self, postgres_db_connection):
        self.postgres_db_connection = postgres_db_connection

    def _run_postgres_query(self, query, params, execute_values=False):
        try:
            with self.postgres_db_connection.connection.cursor() as cursor:
                if execute_values:
                    cursor.executemany(query, params)
                else:
                    cursor.execute(query, params)
                
                if cursor.description:
                    return cursor.fetchall()

                self.postgres_db_connection.connection.commit()
                return None
            
        except Exception as exc:
            self.postgres_db_connection.connection.rollback()
            logger.error("Error occurred while executing query: %s", exc)
            raise RDBMSQueryError(f"Failed to execute query: {exc}")

    def insert_news_sources(self, news_items):
        query = """
            INSERT INTO news_sources (name, portal_url, method_url, fetch_method)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name, portal_url, method_url) DO NOTHING
        """

        values = [
            (item["name"], item["portal_url"], item["method_url"], item["fetch_method"]) 
            for item in news_items
        ]

        self._run_postgres_query(query, values, execute_values=True)

    def get_news_sources(self, source_filters=None):
        query = """
            SELECT id, name, portal_url, method_url, fetch_method
            FROM news_sources
            WHERE method_url = ANY(%s)
        """

        return self._run_postgres_query(query, (source_filters,))