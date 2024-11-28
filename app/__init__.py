from fastapi import FastAPI
from app.api.chat_api import api
from app.api.error_handlers import add_exception_handlers


def create_app():
    app = FastAPI()
    
    # This prevents 307 Temporary Redirects on Request URLs ending in trailing slashes
    for route in api.routes:
        if route.path.endswith("/"):
            route.path = route.path[:-1]

    app.include_router(api)
    add_exception_handlers(app)
    return app
