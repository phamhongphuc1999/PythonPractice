import logging

from src.logging import MY_LOG, INFO, DEBUG, MyLogger

trava_logger = MyLogger("my_logger")


def setup_trava_logging(file_log_level=INFO, console_log_level=MY_LOG):
    """
    Setup trava logging

    :param file_log_level: The file log level
    :param console_log_level: The console log level
    """
    log_formatter = logging.Formatter(
        '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')

    file_handler = logging.FileHandler("trava_api/logging/log-file.log")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(file_log_level)
    trava_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(console_log_level)
    trava_logger.addHandler(console_handler)

    trava_logger.setLevel(DEBUG)


if __name__ == "__main__":
    setup_trava_logging(file_log_level=INFO, console_log_level=MY_LOG)
