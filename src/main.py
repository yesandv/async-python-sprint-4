import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.api.db import db_router
from src.api.urls import url_router
from src.core import app_settings
from src.core.logging_config import logger
from src.utils.middleware import BlackListMiddleware

app = FastAPI(
    title=app_settings.title,
    default_response_class=ORJSONResponse,
    redoc_url=None,
)

middleware = BlackListMiddleware(black_list=app_settings.black_list)

app.add_middleware(BaseHTTPMiddleware, dispatch=middleware)
app.include_router(url_router)
app.include_router(db_router)

if __name__ == "__main__":
    logger.info(
        "Server is starting at %s:%s", app_settings.host, app_settings.port
    )
    uvicorn.run(
        "main:app",
        host=app_settings.host,
        port=app_settings.port,
        loop="asyncio",
        reload=True,
    )
