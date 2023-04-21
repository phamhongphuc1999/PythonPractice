from app.database.base_connector import MongoBaseConnector, ConnectionOption
from app.database.mongo_model.employee_model import EmployeeModel
from app.database.mongo_model.production_model import ProductionModel


class CollectionModel:
    def __init__(
        self, connection: MongoBaseConnector = None, option: ConnectionOption = None
    ):
        self.employee = EmployeeModel(connection=connection, option=option)
        self.production = ProductionModel(connection=connection, option=option)
