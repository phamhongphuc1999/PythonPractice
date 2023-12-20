from pymongo import UpdateOne

from app import AppConfig
from app.database.base_connector import MongoBaseConnector, ConnectionOption
from app.database.base_model import MongoBaseModel
from app.database.database_object.employee_object import (
    EmployeeObject,
    EmployeeMongoObject,
)
from app.services.logger_service import app_logger


class EmployeeModel(MongoBaseModel):
    def __init__(self, connection: MongoBaseConnector = None, option: ConnectionOption = None):
        super().__init__(connection, option)
        _connection = connection.get_connection()
        database = _connection[AppConfig.Global.Mongo.DATABASE_NAME]
        self._employee_collection = database[AppConfig.Global.Mongo.EMPLOYEE_COLLECTION]

    def insert(self, username: str, password: str, email: str):
        try:
            _id = self._employee_collection.insert_one(
                EmployeeObject.get_mongo_data(username=username, password=password, email=email)
            )
        except Exception as error:
            app_logger.error(error)
        return None

    def upsert(self, username: str, data: EmployeeMongoObject):
        try:
            result = self._employee_collection.update_one({"username": username}, data.get_data(), upsert=True)
            return {
                "id": result.upserted_id,
                "modified": result.modified_count,
                "matched": result.matched_count,
            }
        except Exception as error:
            app_logger.error(error)
        return None

    def bulk_upsert(self, data: list[EmployeeMongoObject]):
        try:
            _requests = []
            for item in data:
                if item.username:
                    _requests.append(UpdateOne({"username": item.username}, item.get_data(), upsert=True))
            result = self._employee_collection.bulk_write(_requests, ordered=True)
            return result.bulk_api_result
        except Exception as error:
            app_logger.error(error)
        return None
