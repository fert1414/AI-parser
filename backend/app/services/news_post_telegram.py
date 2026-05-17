import requests

from app.core.logger import logger

class NewsTelegramNotifier:
    def __init__(self, telegram_bot_token, telegram_chat_id):
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id

    def send_message(self, news):
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"

        for item in news:
            title = item.get("title", "No Title")
            description = item.get("content", "No content")
            link = item.get("link", "")

            message = f"{title}\n\n{description}\n\nRead more: {link}"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": message
            }

            response = requests.post(
                url,
                json=payload,
                timeout=15,
                verify=False
            )

            if response.status_code != 200:
                logger.error(f"Failed to send message: {response.text}")