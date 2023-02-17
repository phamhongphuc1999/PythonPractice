import mysql.connector
from app.database.base_connector import BaseConnector, ConnectionOption
from app.database.model.base_model import BaseModel
from app.services.logger_service import app_logger

GET_PRODUCTION_SCRIPT = "SELECT * FROM Production WHERE name = '{name}';"


class ProductionModel(BaseModel):
    def __init__(self, connection: BaseConnector = None, option: ConnectionOption = None):
        super().__init__(connection, option)

    def get_production(self, production_name: str):
        try:
            _cursor = self.connection.get_cursor()
            _cursor.execute(GET_PRODUCTION_SCRIPT.format(name=production_name))
            production_data = []
            for index, name, amount, employeeId in _cursor:
                production_data.append({"name": name, "amount": amount, "employeeId": employeeId})
            _cursor.close()
            return production_data
        except mysql.connector.Error as error:
            app_logger.error(str(error))
        except Exception as error:
            app_logger.error(str(error))
        return None
