from app.core.logger import logger
from app.core.exceptions import SourceAgentError

from app.services.rss_analyzer import RSSAnalyzer

class SourceAgent:
    def __init__(self):
        pass

    def analyze_sources(self, source_links):
        logger.info(f"Start analyzing sources...")
        
        try:
            rss_analyzer = RSSAnalyzer()

            result = []
            for source_link in source_links:
                rss_feed = rss_analyzer.analyze_link(source_link)

                if rss_feed is None:
                    logger.info(f"Can't find rss feed for this url {source_link}")
                    continue
                
                result.append({
                    "source_link": str(source_link),
                    "rss_link": rss_feed
                })

            return result

        except Exception as exc:
            logger.error(f"Error analyzing source: {exc}")
            return None