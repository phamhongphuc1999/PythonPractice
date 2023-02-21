from sanic import Sanic
from sanic_cors import CORS

from app.config import AppConfig
from app.controllers import global_blueprint
from app.controllers.bep20_controller import bep20_blueprint
from app.controllers.employee_controller import employee_blueprint
from app.controllers.production_controller import production_blueprint
from app.controllers.telegram_controller import telegram_blueprint
from sanic_openapi import openapi3_blueprint
from app.misc.log import log


def _register_extensions(sanic_app: Sanic):
    from app import extensions

    extensions.cors = CORS(sanic_app, resources={r"/*": {"origins": "*"}})


def _register_hooks(sanic_app: Sanic):
    from app.hooks.request_context import after_request

    sanic_app.register_middleware(after_request, "response")


def create_app(*config_cls) -> Sanic:
    log(
        message="Sanic application initialized with {}".format(
            ", ".join([config.__name__ for config in config_cls])
        ),
        keyword="INFO",
    )

    sanic_app = Sanic(AppConfig.Global.App.NAME)
    for _config in config_cls:
        sanic_app.config.update_config(_config)

    _register_extensions(sanic_app)
    _register_hooks(sanic_app)
    return sanic_app


def create_routes(sanic_app: Sanic, **kwargs):
    sanic_app.blueprint(openapi3_blueprint)
    sanic_app.blueprint(global_blueprint)
    for key, value in kwargs.items():
        if key == "employee" and value:
            sanic_app.blueprint(employee_blueprint)
        elif key == "production" and value:
            sanic_app.blueprint(production_blueprint)
        elif key == "telegram" and value:
            sanic_app.blueprint(telegram_blueprint)
        elif key == "bep20" and value:
            sanic_app.blueprint(bep20_blueprint)
