from typing import Union

import mysql.connector
from mysql.connector import errorcode, CMySQLConnection, MySQLConnection
from mysql.connector.cursor import MySQLCursor
from app.services.logger_service import app_logger


class ConnectionOption:
    def __init__(
        self, host: str, port: str, username: str, password: str, database: str
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database


class BaseConnector:
    def __init__(self, option: ConnectionOption):
        self.option = option
        self._connect()

    def _connect(self):
        try:
            host = self.option.host
            port = self.option.port
            username = self.option.username
            password = self.option.password
            database = self.option.database
            self._connection = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database,
            )
            app_logger.info(f"Connected to database: {host}:{port}")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                app_logger.error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                app_logger.error("Database does not exist")
            else:
                app_logger.error(err)
            raise err
        except Exception as err:
            raise err

    def reconnect(self):
        self._connect()

    def get_connection(self) -> Union[CMySQLConnection, MySQLConnection]:
        return self._connection

    def get_cursor(self) -> MySQLCursor:
        return self._connection.cursor(buffered=True)

    def close_connection(self):
        self._connection.close()
