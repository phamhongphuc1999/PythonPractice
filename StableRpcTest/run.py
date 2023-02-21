import os
import sys

from service.logger_service import app_logger
from service.telegram_service import send_telegram_message

if __name__ == "__main__":
    _arg = sys.argv
    app_logger.info(_arg)
    bot_id = _arg[1]
    chat_id = _arg[2]
    os.system(
        f"python3 main.py bsc {bot_id} {chat_id} & python3 main.py ftm {bot_id} {chat_id} & python3 main.py eth {bot_id} {chat_id}"
    )
