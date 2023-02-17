from aiohttp.web_response import json_response

from app.config.constants import AppConfig
from app.service.Summarization import decode
from app.service.decorate import get_body_request
from app.service.make_token import tokenize_stories, get_article


async def ping_server(request):
    try:
        return json_response({"message": "ping success!"})
    except Exception as error:
        return json_response({"status": 0, "error": str(error)})


async def tokenize(request):
    try:
        body = await get_body_request(request)
        _tokenize_data = tokenize_stories(body["story"])
        _article_data = get_article(_tokenize_data)
        return json_response({"story": body["story"], "tokenize": _tokenize_data, "article": _article_data})
    except Exception as error:
        return json_response({"status": 0, "error": str(error)})


async def make_summary(request):
    try:
        body = await get_body_request(request)
        story = body["story"]
        _data = decode(story, AppConfig.PRE_TRAIN_MODEL, 1, 30)
        return json_response({"story": _data})
    except Exception as error:
        return json_response({"status": 0, "error": str(error)})
