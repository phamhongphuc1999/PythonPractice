from typing import List

from sanic import Request


def require_params(request: Request, params: List[str]):
    for param in params:
        if not request.args.get(param):
            raise Exception(f"Require param: {param}")
