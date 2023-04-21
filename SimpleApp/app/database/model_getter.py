from app import AppConfig
from app.database.base_connector import (
    SqlBaseConnector,
    ConnectionOption,
    MongoBaseConnector,
)
from app.database.mongo_model import CollectionModel
from app.database.sql_model import TableModel


class _SqlGetter:
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
            self._connection = SqlBaseConnector(
                ConnectionOption(host, port, username, password, database)
            )

    def get_model(self) -> TableModel:
        if self._connection is None:
            raise Exception("Database is disconnected")
        if self._model is None:
            self._model = TableModel(connection=self._connection)
        return self._model


class _MongoGetter:
    def __init__(self):
        self._connection = None
        self._model = None

    def connect(self):
        if self._connection is None:
            host = AppConfig.Global.Mongo.HOST
            port = AppConfig.Global.Mongo.PORT
            username = AppConfig.Global.Mongo.USER_NAME
            password = AppConfig.Global.Mongo.PASSWORD
            database = AppConfig.Global.Mongo.DATABASE_NAME
            self._connection = MongoBaseConnector(
                ConnectionOption(host, port, username, password, database)
            )

    def get_model(self):
        if self._connection is None:
            raise Exception("Database is disconnected")
        if self._model is None:
            self._model = CollectionModel(connection=self._connection)
        return self._model


class _ModelGetter:
    SQL = _SqlGetter()
    Mongo = _MongoGetter()


ModelGetter = _ModelGetter()
