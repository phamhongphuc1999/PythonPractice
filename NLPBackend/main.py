import os

from aiohttp import web

from app.config import setup_logging, setup_cors
from app.config.constants import AppConfig
from app.service.Summarization import decode, decode_more
from app.service.make_token import tokenize_stories
from route import setup_routes


def run():
    app = web.Application(client_max_size=20 * 1024**2)
    setup_logging(True, True)
    setup_routes(app)
    setup_cors(app)
    web.run_app(app, host=AppConfig.HOST, port=AppConfig.PORT)


if __name__ == "__main__":
    run()
