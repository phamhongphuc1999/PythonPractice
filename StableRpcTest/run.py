import os
import sys
from service.logger_service import app_logger

if __name__ == "__main__":
    _arg = sys.argv
    app_logger.info(_arg)
    bot_id = _arg[1]
    chat_id = _arg[2]
    case_id = _arg[3]
    if case_id == "1":
        os.system(
            f"python3 case1.py bsc {bot_id} {chat_id} & "
            f"python3 case1.py ftm {bot_id} {chat_id} & "
            f"python3 case1.py eth {bot_id} {chat_id}"
        )
    else:
        os.system(f"python3 case2.py {bot_id} {chat_id}")
