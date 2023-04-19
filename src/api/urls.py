from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from src.core.logging_config import logger
from src.db.db import get_session
from src.schemas.url import FullUrl, ShortUrl, UrlInDB, UrlUpdate
from src.services.short_url import url_crud

url_router = APIRouter(prefix="/urls", tags=["URLs"])


@url_router.post(
    "/shorten",
    response_model=ShortUrl,
    description="Creates a shortened URL. The response is a ShortUrl schema.",
)
async def shorten_url(
        *,
        schema: FullUrl,
        session: AsyncSession = Depends(get_session),
) -> Response:
    logger.info("Shortening %s", schema.full_url)
    return await url_crud.create(session=session, schema=schema)


@url_router.get(
    "/{url_id}",
    response_class=RedirectResponse,
    description="Redirects the user to the corresponding full URL.",
)
async def redirect_url(
        *,
        url_id: str,
        session: AsyncSession = Depends(get_session),
) -> RedirectResponse:
    _url = await url_crud.get(session=session, url_id=url_id)
    if _url.is_taken_down:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Gone")
    url = await url_crud.update(
        session=session, url_id=url_id, clicks=_url.clicks + 1
    )
    logger.info("Redirecting to %s", url.full_url)
    return RedirectResponse(url=url.full_url)


@url_router.get(
    "/{url_id}/status",
    response_model=UrlInDB,
    description="Retrieves the corresponding URL from the database.",
)
async def get_url_status(
        *, url_id: str, session: AsyncSession = Depends(get_session)
) -> Response:
    logger.info("Retrieving %s from the DB", url_id)
    url = await url_crud.get(session=session, url_id=url_id)
    if url.is_taken_down:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Gone")
    return url


@url_router.delete(
    "/{url_id}",
    response_model=UrlUpdate,
    description="Marks the corresponding URL as deleted in the database.",
)
async def delete_url(
        *, url_id: str, session: AsyncSession = Depends(get_session)
) -> Response:
    url = await url_crud.update(
        session=session, url_id=url_id, is_taken_down=True
    )
    if url.is_taken_down:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Gone")
    return url
