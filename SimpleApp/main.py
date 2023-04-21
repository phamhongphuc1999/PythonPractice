from app import create_app, create_routes, AppConfig

from app.config import EnvironmentType
from app.database.model_getter import ModelGetter
from app.services.logger_service import app_logger
from app.services import get_env


def run_server(auto_reload=False):
    sanic_app = create_app()
    create_routes(
        sanic_app,
        employee=AppConfig.Extension.EMPLOYEE_ROUTER,
        production=AppConfig.Extension.PRODUCTION_ROUTER,
        telegram=AppConfig.Extension.TELEGRAM_ROUTE,
        bep20=AppConfig.Extension.BEP20_ROUTE,
    )
    app_logger.info(f"environment: {AppConfig.env}")
    sanic_app.run(
        host=AppConfig.Global.App.HOST,
        port=AppConfig.Global.App.PORT,
        auto_reload=auto_reload,
        debug=False,
        access_log=True,
        workers=4,
    )


if __name__ == "__main__":
    try:
        env = get_env()
        AppConfig.init_env(env)
        if env == EnvironmentType.DEV_DOCKER:
            ModelGetter.SQL.connect()
            run_server()
        elif env == EnvironmentType.DEVELOPMENT:
            ModelGetter.SQL.connect()
            run_server(True)
        elif env == EnvironmentType.BASIC:
            run_server(True)
        else:
            app_logger.error(f"Not found {env}, process is stopped")
    except Exception as error:
        app_logger.error(error)
