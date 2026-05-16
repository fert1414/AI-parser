from backend.app.db.RDBMS_db.repositories.news_sources import NewsSourceRepository
from backend.app.core.config import settings

def insert_sample_news_sources(postgres_db_connection):
    news_source_repository = NewsSourceRepository(postgres_db_connection)

    sample_news_sources = [
        {
            "name": "RBK News",
            "url": "https://rssexport.rbc.ru/rbcnews/news/30/full.rss",
            "fetch_method": "rss"
        }
    ]

    news_source_repository.insert_news_sources(sample_news_sources)

insert_sample_news_sources(settings.POSTGRES_DB_CONNECTION)