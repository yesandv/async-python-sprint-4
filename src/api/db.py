from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session
from src.services.short_url import url_crud

db_router = APIRouter(prefix="/db", tags=["DB"])


@db_router.get("/ping")
async def ping(session: AsyncSession = Depends(get_session)) -> dict:
    return await url_crud.ping(session=session)
