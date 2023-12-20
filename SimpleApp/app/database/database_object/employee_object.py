ADD_USER_SCRIPT = "INSERT INTO Employees (username, password, email) VALUE ({username}, {password}, {email});"
SELECT_USER_SCRIPT = "SELECT * FROM Employees WHERE username = '{username}' AND password = '{password}';"
SELECT_USER_BY_USERNAME_SCRIPT = "SELECT * FROM Employees WHERE username = '{username}';"


class EmployeeMongoObject:
    def __init__(self, username: str = None, password: str = None, email: str = None):
        self.username = username
        self.password = password
        self.email = email

    def get_data(self):
        return EmployeeObject.get_mongo_data(username=self.username, password=self.password, email=self.email)


class EmployeeObject:
    @staticmethod
    def get_mongo_data(username: str = None, password: str = None, email: str = None):
        result = {}
        if username:
            result["username"] = username
        if password:
            result["password"] = password
        if email:
            result["email"] = email
        return result

    @staticmethod
    def get_sql_add_user(username: str, password: str, email: str):
        return ADD_USER_SCRIPT.format(username=username, password=password, email=email)

    @staticmethod
    def get_sql_select_user(username: str, password: str = None):
        if password:
            return SELECT_USER_SCRIPT.format(username=username, password=password)
        else:
            return SELECT_USER_BY_USERNAME_SCRIPT.format(username=username)
