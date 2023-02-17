from aiohttp import web

from app.controllers.nlp_controller import *


def setup_routes(app: web.Application):
    app.router.add_route("GET", "/ping", ping_server)
    app.router.add_route("POST", "/tokenize-message", tokenize)
    app.router.add_route("POST", "/summary", make_summary)
