from fastapi import APIRouter, Depends
from fastapi.openapi.models import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from src.core.logging_config import logger
from src.db.db import get_session
from src.schemas.url import FullUrl, ShortUrl, UrlInDB, UrlUpdate
from src.services.short_url import url_crud
from src.utils.exceptions import GoneException

url_router = APIRouter(prefix="/urls", tags=["URLs"])


@url_router.post("/shorten", response_model=ShortUrl)
async def shorten_url(
        *,
        schema: FullUrl,
        session: AsyncSession = Depends(get_session),
) -> Response:
    logger.info("Shortening %s", schema.full_url)
    return await url_crud.create(session=session, schema=schema)


@url_router.get("/{url_id}", response_class=RedirectResponse)
async def redirect_url(
        *,
        url_id: str,
        session: AsyncSession = Depends(get_session),
) -> RedirectResponse:
    _url = await url_crud.get(session=session, url_id=url_id)
    GoneException(_url)
    url = await url_crud.update(
        session=session, url_id=url_id, clicks=_url.clicks + 1
    )
    logger.info("Redirecting to %s", url.full_url)
    return RedirectResponse(url=url.full_url)


@url_router.get("/{url_id}/status", response_model=UrlInDB)
async def get_url_status(
        *, url_id: str, session: AsyncSession = Depends(get_session)
) -> Response:
    logger.info("Retrieving %s from the DB", url_id)
    url = await url_crud.get(session=session, url_id=url_id)
    GoneException(url)
    return url


@url_router.delete("/{url_id}", response_model=UrlUpdate)
async def delete_url(
        *, url_id: str, session: AsyncSession = Depends(get_session)
) -> Response:
    url = await url_crud.update(
        session=session, url_id=url_id, is_taken_down=True
    )
    GoneException(url)
    return url
