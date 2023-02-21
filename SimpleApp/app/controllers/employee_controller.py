from sanic import Blueprint, Request

from app import AppConfig
from app.apis.api_response import ok_json, bad_request_json
from app.apis.api_wrapper import validate_body_with_json_schema
from app.database.model_getter import ModelGetter

employee_blueprint = Blueprint("employee_blueprint", url_prefix="/employee")


@employee_blueprint.post("/register")
@validate_body_with_json_schema(AppConfig.Schema.User.ADD_USER)
async def register_user(request: Request):
    try:
        body = request.json
        username = body["username"]
        password = body["password"]
        email = body["email"]
        result = ModelGetter.get_model().employee.add_new_user(
            username, password, email
        )
        return ok_json(result)
    except Exception as error:
        return bad_request_json(str(error))


@employee_blueprint.post("/login")
@validate_body_with_json_schema(AppConfig.Schema.User.LOGIN)
async def login_app(request: Request):
    try:
        body = request.json
        username = body["username"]
        password = body["password"]
        user_data = ModelGetter.get_model().employee.get_employee_by_username_password(
            username, password
        )
        return ok_json({"data": user_data})
    except Exception as error:
        return bad_request_json(str(error))
