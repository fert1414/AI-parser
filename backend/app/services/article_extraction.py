import re

import requests
import trafilatura
from bs4 import BeautifulSoup

from backend.app.core.logger import logger

class ArticleExtractor:
    def __init__(self, timeout=15):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0 Safari/537.36"
            )
        }

    def extract_from_url(self, url: str) -> dict:
        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                logger.warning(f"Failed to download article from {url}")
                return {"full_text": ""}
            
        except requests.RequestException as exc:
            logger.error(f"Failed to fetch article from {url}: {exc}")
            return {"full_text": ""}

        full_text = trafilatura.extract(downloaded)

        return {"full_text": full_text}