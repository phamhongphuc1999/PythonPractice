from app import AppConfig
from app.database.base_connector import BaseConnector, ConnectionOption
from app.database.model import TableModel


class _ModelGetter:
    def __init__(self):
        self._connection = None
        self._model = None

    def connect(self):
        if self._connection is None:
            host = AppConfig.Global.SQL.HOST
            port = AppConfig.Global.SQL.PORT
            username = AppConfig.Global.SQL.USER_NAME
            password = AppConfig.Global.SQL.PASSWORD
            database = AppConfig.Global.SQL.DATABASE_NAME
            self._connection = BaseConnector(
                ConnectionOption(host, port, username, password, database)
            )

    def get_model(self) -> TableModel:
        if self._connection is None:
            raise Exception("Database is disconnected")
        if self._model is None:
            self._model = TableModel(connection=self._connection)
        return self._model


ModelGetter = _ModelGetter()
