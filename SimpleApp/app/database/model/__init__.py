from app.database.base_connector import BaseConnector, ConnectionOption
from app.database.model.employee_model import EmployeeModel
from app.database.model.production_model import ProductionModel


class TableModel:
    def __init__(self, connection: BaseConnector = None, option: ConnectionOption = None):
        self.employee = EmployeeModel(connection=connection, option=option)
        self.production = ProductionModel(connection=connection, option=option)
