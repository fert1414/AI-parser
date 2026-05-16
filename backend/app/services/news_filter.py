from backend.app.core.logger import logger

class NewsFilter:
    def __init__(self, news, theme_filters=None):
        self.news = news
        self.theme_filters = theme_filters

    def filter_news(self):
        if not self.theme_filters:
            return self.news

        filtered_news = []
        for item in self.news:
            