from app.config.constant import EnvironmentType


class ExtensionConfig:
    def __init__(self):
        self.EMPLOYEE_ROUTER = True
        self.PRODUCTION_ROUTER = True
        self.TELEGRAM_ROUTE = True
        self.BEP20_ROUTE = True

    def init_env(self, _env: EnvironmentType):
        if _env == EnvironmentType.BASIC:
            self.EMPLOYEE_ROUTER = False
            self.PRODUCTION_ROUTER = False
