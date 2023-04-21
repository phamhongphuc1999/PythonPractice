from sanic import Blueprint, Request

from app.apis import require_params
from app.apis.api_response import ok_json, bad_request_json
from app.database.model_getter import ModelGetter

production_blueprint = Blueprint("Production", url_prefix="/production")


@production_blueprint.post("/")
async def login_app(request: Request):
    try:
        require_params(request, ["name"])
        production_name = request.args.get("name")
        user_data = ModelGetter.SQL.get_model().production.get_production(
            production_name
        )
        return ok_json({"data": user_data})
    except Exception as error:
        return bad_request_json(str(error))
