from fastapi import FastAPI

from cctv_ai.api.routes import router
from cctv_ai.core.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.service_name, version="0.1.0")
    app.include_router(router)
    return app
