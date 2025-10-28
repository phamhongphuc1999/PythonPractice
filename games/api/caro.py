from fastapi import APIRouter

caro_route = APIRouter(prefix="/caro", tags=["Caro"])

@caro_route.get("/move")
def caro_move():
    return {"message": "Caro move"}
