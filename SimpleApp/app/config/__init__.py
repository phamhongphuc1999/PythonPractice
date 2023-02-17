from app.config.extension_config import ExtensionConfig
from app.config.global_config import GlobalConfig
from app.config.constant import EnvironmentType
from app.config.network_config import NetworkConfig
from app.config.schema import SchemaConfig


class _AppConfig:
    def __init__(self):
        self.Global = GlobalConfig()
        self.Extension = ExtensionConfig()
        self.Schema = SchemaConfig()
        self.Network = NetworkConfig()
        self.env = None

    def init_env(self, _env: EnvironmentType):
        self.env = _env
        self.Global.init_env(_env)
        self.Extension.init_env(_env)


AppConfig = _AppConfig()
