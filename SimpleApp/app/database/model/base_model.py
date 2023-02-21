from app.database.base_connector import BaseConnector, ConnectionOption


class BaseModel:
    def __init__(
        self, connection: BaseConnector = None, option: ConnectionOption = None
    ):
        if connection:
            self.connection = connection
        elif option:
            self.connection = BaseConnector(option)
        else:
            raise Exception("Missing connection option")
