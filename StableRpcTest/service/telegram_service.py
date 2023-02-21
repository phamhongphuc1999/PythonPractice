import json

import requests

from service.logger_service import app_logger


def send_telegram_message(message, bot_id, chat_id):
    url = f"https://api.telegram.org/bot{bot_id}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    try:
        response = requests.request("POST", url, params=data)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as error:
        app_logger.error(str(error))
        return False
