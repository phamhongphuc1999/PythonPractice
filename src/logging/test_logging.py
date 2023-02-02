import logging

from src.logging import MY_LOG, INFO, DEBUG, MyLogger, CustomFormatter

trava_logger = MyLogger("my_logger")


def setup_trava_logging(file_log_level=INFO, console_log_level=DEBUG):
    """
    Setup trava logging

    :param file_log_level: The file log level
    :param console_log_level: The console log level
    """
    log_formatter = logging.Formatter(
        "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s", "%m-%d %H:%M:%S"
    )

    custom_formatter = CustomFormatter()

    file_handler = logging.FileHandler("log-file.log")
    file_handler.setFormatter(custom_formatter)
    file_handler.setLevel(file_log_level)
    trava_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(custom_formatter)
    console_handler.setLevel(console_log_level)
    trava_logger.addHandler(console_handler)

    trava_logger.setLevel(DEBUG)


if __name__ == "__main__":
    setup_trava_logging(file_log_level=INFO, console_log_level=MY_LOG)
    trava_logger.info("12345")
    trava_logger.error("123455555")
