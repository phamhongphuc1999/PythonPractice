import mysql.connector

from app.database.base_model import SqlBaseModel
from app.database.database_object.employee_object import EmployeeObject
from app.services.logger_service import app_logger
from app.database.base_connector import SqlBaseConnector, ConnectionOption


class EmployeeModel(SqlBaseModel):
    def __init__(self, connection: SqlBaseConnector = None, option: ConnectionOption = None):
        super().__init__(connection, option)

    def add_new_user(self, username: str, password: str, email: str):
        try:
            _cursor = self.connection.get_cursor()
            _cursor.execute(EmployeeObject.get_sql_select_user(username=username))
            if _cursor.rowcount > 0:
                return f"{username} has been already exists"
            _cursor.execute(EmployeeObject.get_sql_add_user(username=username, password=password, email=email))
            _cursor.close()
            return "success"
        except mysql.connector.Error as error:
            app_logger.error(str(error))
        except Exception as error:
            app_logger.error(str(error))
        return None

    def get_employee_by_username_password(self, username: str, password: str):
        try:
            _cursor = self.connection.get_cursor()
            _cursor.execute(EmployeeObject.get_sql_select_user(username=username, password=password))
            employee_data = []
            for index, username, password, email in _cursor:
                employee_data.append({"username": username, "password": password, "email": email})
            _cursor.close()
            return employee_data
        except mysql.connector.Error as error:
            app_logger.error(str(error))
        except Exception as error:
            app_logger.error(str(error))
        return None
