from aiohttp.web_request import Request

pagination = ["page_size", "page_index"]


async def get_body_request(request):
    result = await Request.json(request)
    return result
