from app.database.base_connector import SqlBaseConnector, ConnectionOption
from app.database.sql_model.employee_model import EmployeeModel
from app.database.sql_model.production_model import ProductionModel


class SqlModel:
    def __init__(self, connection: SqlBaseConnector = None, option: ConnectionOption = None):
        self.employee = EmployeeModel(connection=connection, option=option)
        self.production = ProductionModel(connection=connection, option=option)
