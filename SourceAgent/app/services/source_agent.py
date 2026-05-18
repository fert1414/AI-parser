from app.core.logger import logger
from app.core.exceptions import SourceAgentError
from app.core.config import settings

from app.services.rss_analyzer import RSSAnalyzer

from ML_service.clients.yandexgpt_api import YandexGPTClient

class SourceAgent:
    def __init__(self):
        pass

    def analyze_sources(self, source_links):
        logger.info(f"Start analyzing sources...")

        llm = YandexGPTClient(
            settings.yandexgpt_api_url, 
            settings.yandexgpt_api_key, 
            settings.yandexgpt_folder_id
        )
        
        try:
            rss_analyzer = RSSAnalyzer(llm)

            result = []
            for source_link in source_links:
                source_link = str(source_link)
                rss_feed_info = rss_analyzer.analyze_link(source_link)

                if rss_feed_info is None:
                    logger.info(f"Can't find rss feed for this url {source_link}")
                
                result.append(rss_feed_info)

            return result

        except Exception as exc:
            logger.error(f"Error analyzing source: {exc}")
            return None