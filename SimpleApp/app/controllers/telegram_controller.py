import json

import requests
from sanic import Blueprint, Request
from sanic_openapi import openapi

from app.apis.api_response import ok_json, bad_request_json
from app.config.constant import TELEGRAM_GET_METHODS, ALL_METHODS
from app.apis import require_params


class TelegramApi:
    BASE_URL = "https://api.telegram.org/bot"

    @staticmethod
    def request(method: str, url: str, *args, **kwargs):
        print(f"{TelegramApi.BASE_URL}{url}")
        response = requests.request(
            method=method, url=f"{TelegramApi.BASE_URL}{url}", *args, **kwargs
        )
        _data = json.loads(response.text)
        if _data["ok"]:
            return _data["result"]
        else:
            if "description" in _data:
                raise Exception(_data["description"])
            raise Exception("Something wrong...")

    @staticmethod
    def get(url: str, *args, **kwargs):
        return TelegramApi.request("get", url, *args, **kwargs)

    @staticmethod
    def post(url: str, *args, **kwargs):
        return TelegramApi.request("post", url, *args, **kwargs)

    @staticmethod
    def delete(url: str, *args, **kwargs):
        return TelegramApi.request("delete", url, *args, **kwargs)


def _build_params(**kwargs):
    params = {}
    for key, value in kwargs.items():
        if value:
            params[key] = value
    return params


telegram_blueprint = Blueprint("Telegram", url_prefix="/telegram")


@telegram_blueprint.get("/getUpdates")
@openapi.summary("Get bot updates")
@openapi.parameter("botId", str, location="query")
async def get_updates(request: Request):
    try:
        require_params(request, ["botId"])
        bot_id = request.args.get("botId")
        chat_id = request.args.get("chatId")
        result = TelegramApi.get(f"{bot_id}/getUpdates")
        if chat_id:
            filter_result = []
            for item in result:
                message = item.get("message")
                if message:
                    chat = message.get("chat")
                    if chat:
                        if str(chat.get("id")) == chat_id:
                            filter_result.append(item)
            return ok_json(filter_result)
        return ok_json(result)
    except Exception as error:
        return bad_request_json(str(error))


@telegram_blueprint.get("/getWebhookInfo")
async def get_web_hook_info(request: Request):
    try:
        require_params(request, ["botId"])
        bot_id = request.args.get("botId")
        result = TelegramApi.get(f"{bot_id}/getWebhookInfo")
        return ok_json(result)
    except Exception as error:
        return bad_request_json(str(error))


@telegram_blueprint.post("/setWebhook")
async def get_web_hook_info(request: Request):
    try:
        require_params(request, ["botId", "url"])
        bot_id = request.args.get("botId")
        url = request.args.get("url")
        result = TelegramApi.get(f"{bot_id}/setWebhook", params={"url": url})
        return ok_json(result)
    except Exception as error:
        return bad_request_json(str(error))


@telegram_blueprint.get("/getMethods")
async def get_methods(request: Request):
    try:
        return ok_json({"getMethods": TELEGRAM_GET_METHODS, "allMethods": ALL_METHODS})
    except Exception as error:
        return bad_request_json(str(error))


@telegram_blueprint.get("/getBots")
async def get_bots(request: Request):
    try:
        require_params(request, ["botId"])
        bot_id = request.args.get("botId")
        method = request.args.get("method")
        if method is None:
            method = "getChat"
        elif method not in TELEGRAM_GET_METHODS:
            raise Exception(
                f"Not found get method: {method}. Method must be in {TELEGRAM_GET_METHODS}"
            )
        params = _build_params(chat_id=request.args.get("chatId"))
        result = TelegramApi.get(f"{bot_id}/{method}", params=params)
        return ok_json(result)
    except Exception as error:
        return bad_request_json(str(error))


@telegram_blueprint.post("/setMyCommands")
async def set_my_commands(request: Request):
    try:
        require_params(request, ["botId", "commands"])
        bot_id = request.args.get("botId")
        params = _build_params(
            commands=request.args.get("commands"),
            scope=request.args.get("scope"),
            language_code=request.args.get("language_code"),
        )
        result = TelegramApi.post(f"{bot_id}/setMyCommands", params=params)
        return ok_json(result)
    except Exception as error:
        return bad_request_json(str(error))


@telegram_blueprint.delete("/deleteMyCommands")
async def delete_my_commands(request: Request):
    try:
        require_params(request, ["botId"])
        bot_id = request.args.get("botId")
        params = _build_params(
            scope=request.args.get("scope"),
            language_code=request.args.get("language_code"),
        )
        result = TelegramApi.delete(f"{bot_id}/deleteMyCommands", params=params)
        return ok_json(result)
    except Exception as error:
        return bad_request_json(str(error))
