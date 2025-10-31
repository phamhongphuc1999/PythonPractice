from fastapi import FastAPI
from api import caro


def hello():
    return {"message": "Hello world"}


def create_fastapi():
    app = FastAPI()
    return app


def create_routes(app: FastAPI):
    app.add_api_route(path="/hello", endpoint=hello, methods=["GET"], tags=["Hello"])

    app.include_router(caro.caro_route)
