from functools import wraps

import jwt
from jsonschema import validate, ValidationError
from sanic import Request

from app import AppConfig
from app.apis.api_response import bad_request_json


def required_param(param_list: list):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(request: Request, *args, **kwargs):
            for _param in param_list:
                _value = request.args.get(_param)
                if not _value:
                    return bad_request_json(f"{_param} is required")
            return await fn(request, *args, **kwargs)

        return wrapper

    return decorator


def _check_jwt_token(request: Request):
    jwt_token = request.token
    if not jwt_token:
        return False
    try:
        _user_data = jwt.decode(jwt_token, AppConfig.Global.Auth.SECRET_KEY, algorithms=["HS256"])
        return _user_data
    except jwt.exceptions.InvalidTokenError:
        return False


def authorization():
    def decorator(fn):
        @wraps(fn)
        async def wrapper(request: Request, *args, **kwargs):
            _user_data = _check_jwt_token(request)
            if _user_data:
                return await fn(request, _user_data, *args, **kwargs)
            else:
                return bad_request_json("You are unauthorized")

        return wrapper

    return decorator


def validate_body_with_json_schema(json_schema: dict):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(request: Request, *args, **kwargs):
            try:
                validate(request.json, json_schema)
            except ValidationError as error:
                return bad_request_json(error.message)
            return await fn(request, *args, **kwargs)

        return wrapper

    return decorator
