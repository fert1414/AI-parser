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

# insert_sample_news_sources(settings.POSTGRES_DB_CONNECTION)

from backend.app.clients.gigachat_client import GigaChatClient

# gc = GigaChatClient(settings.gigachat_api_url, settings.gigachat_api_key)
# gc.print_available_models()
# print(gc.get_balance())
# emb = gc.create_embeddings("GigaEmbeddings-3B-2025-09", "Привет, мир!").get("data")[0].get("embedding", [])
# print(emb, len(emb))

from backend.app.clients.openrouter_client import OpenRouterClient
oc = OpenRouterClient(settings.openrouter_api_url, settings.openrouter_api_key)
# emb = oc.create_embeddings(["Привет, мир!", "Пока свет!"]).get("data", [])
# for e in emb:
#     print(len(e.get("embedding", [])))
# print(emb, len(emb))
models = oc.get_models([":free"])
for model in models:
    print(model.get("id"))#, model.get("architecture"))