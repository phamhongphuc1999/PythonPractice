import json
import os

from app.config.constant import EnvironmentType

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class GlobalConfig:
    def __init__(self):
        self.SQL = self._SQL()
        self.Mongo = self._Mongo()

    def init_env(self, _env: EnvironmentType):
        self.SQL.init_env(_env)

    class ABI:
        BEP20_ABI = json.loads(open(f"{basedir}/resources/bep20_abi.json").read())

    class App:
        NAME = "sanic_simple_api"
        PORT = 8000
        HOST = "0.0.0.0"

    class _SQL:
        def __init__(self):
            self.PORT = 3306
            self.USER_NAME = "root"
            self.PASSWORD = "sanic"
            self.DATABASE_NAME = "sanic_app"
            self.HOST = "127.0.0.1"

        def init_env(self, _env: EnvironmentType):
            if _env == EnvironmentType.DEVELOPMENT:
                self.HOST = "127.0.0.1"
            elif _env == EnvironmentType.DEV_DOCKER:
                self.HOST = "docker.for.mac.host.internal"
            elif _env != EnvironmentType.BASIC:
                raise Exception(f"Not found {_env} environment config")

    class _Mongo:
        def __init__(self):
            self.PORT = 27013
            self.USER_NAME = "root"
            self.PASSWORD = "sanic"
            self.DATABASE_NAME = "sanic_app"
            self.HOST = "127.0.0.1"

        def init_env(self, _env: EnvironmentType):
            if _env == EnvironmentType.DEVELOPMENT:
                self.HOST = "127.0.0.1"
            elif _env == EnvironmentType.DEV_DOCKER:
                self.HOST = "docker.for.mac.host.internal"
            elif _env != EnvironmentType.BASIC:
                raise Exception(f"Not found {_env} environment config")
