from app.database.base_connector import MongoBaseConnector, ConnectionOption
from app.database.base_model import MongoBaseModel


class ProductionModel(MongoBaseModel):
    def __init__(self, connection: MongoBaseConnector = None, option: ConnectionOption = None):
        super().__init__(connection, option)
