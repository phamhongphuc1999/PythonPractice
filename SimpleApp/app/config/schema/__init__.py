from app.config.schema.telegram_schema import _TelegramSchemaConfig
from app.config.schema.user_schema import _UserSchemaConfig


class SchemaConfig:
    User = _UserSchemaConfig()
    Telegram = _TelegramSchemaConfig()
