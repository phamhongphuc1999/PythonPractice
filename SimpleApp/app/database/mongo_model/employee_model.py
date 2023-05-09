from app.database.base_connector import MongoBaseConnector, ConnectionOption
from app.database.base_model import MongoBaseModel


class EmployeeModel(MongoBaseModel):
    def __init__(self, connection: MongoBaseConnector = None, option: ConnectionOption = None):
        super().__init__(connection, option)

    def add_new_user(self, username: str, password: str, email: str):
        pass
