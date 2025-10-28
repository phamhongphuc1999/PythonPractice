from api import create_fastapi, create_routes

app = create_fastapi()
create_routes(app)
