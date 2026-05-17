from sklearn.metrics.pairwise import cosine_similarity

from backend.app.core.logger import logger

from backend.app.services.article_extraction import ArticleExtractor
from backend.app.prompts.filter_prompts import create_filter_prompt

class NewsFilter:
    def __init__(self, AI_client):
        self.AI_client = AI_client
        self.article_extractor = ArticleExtractor()

    def filter_news(self, news, theme_filters=None):
        if not theme_filters:
            return news
        
        news_text = []
        for article in news:
            content = self.article_extractor.extract_from_url(article.get("link", ""))
            news_text.append({
                "title": article.get("title", ""),
                "content": content
            })

        filtered_news = []
        for index in range(0, len(news_text), 5):
            batch = news_text[index:index+5]

            prompt = create_filter_prompt(batch, theme_filters, len(batch))
            result = self.AI_client.ask_json(prompt)

            scores = result.get("relevance", [0.0] * len(batch))

            all_info_batch = news[index:index+5]
            for article, score in zip(all_info_batch, scores):
                
                if score >= 0.5:
                    filtered_news.append(article)

        return filtered_news
        