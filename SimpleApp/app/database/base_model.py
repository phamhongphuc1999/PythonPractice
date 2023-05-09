from app.database.base_connector import (
    SqlBaseConnector,
    ConnectionOption,
    MongoBaseConnector,
)


class SqlBaseModel:
    def __init__(self, connection: SqlBaseConnector = None, option: ConnectionOption = None):
        if connection:
            self.connection = connection
        elif option:
            self.connection = SqlBaseConnector(option)
        else:
            raise Exception("Missing connection option")


class MongoBaseModel:
    def __init__(self, connection: MongoBaseConnector = None, option: ConnectionOption = None):
        if connection:
            self.connection = connection
        elif option:
            self.connection = MongoBaseConnector(option)
        else:
            raise Exception("Missing connection option")
