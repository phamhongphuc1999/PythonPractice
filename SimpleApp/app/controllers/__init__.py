from sanic import Blueprint, Request

from app.apis.api_response import ok_json, bad_request_json

global_blueprint = Blueprint("global_blueprint", url_prefix="/")


@global_blueprint.get("/ping")
async def ping_server(request: Request):
    try:
        return ok_json({"status": "ok"})
    except Exception as error:
        return bad_request_json(str(error))


@global_blueprint.post("/test")
async def ping_server(request: Request):
    try:
        print(request.json)
        return ok_json({"status": "ok"})
    except Exception as error:
        return bad_request_json(str(error))
