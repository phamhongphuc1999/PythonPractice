import aiohttp_cors
import logging


def setup_cors(app):
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        },
    )
    for route in list(app.router.routes()):
        cors.add(route)


def setup_logging(log_file, log_console):
    log_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s-%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    root_logger = logging.getLogger()

    if log_file:
        file_handler = logging.FileHandler("logFile.txt")
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

    if log_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)
        root_logger.setLevel(logging.INFO)
        return root_logger
