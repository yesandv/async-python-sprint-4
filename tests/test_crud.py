from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UrlModel


@pytest.mark.asyncio
async def test_ping(client: AsyncClient):
    response = await client.get("db/ping")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Database is up and running"}


@pytest.mark.asyncio
async def test_shorten_url(client: AsyncClient):
    full_url = "https://www.google.com"
    response = await client.post("urls/shorten", json={"full_url": full_url})
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["id"]) == 7


@pytest.mark.asyncio
async def test_shorten_url_id(test_session: AsyncSession, client: AsyncClient):
    full_url = "https://www.google.com/maps/"
    statement = select(UrlModel).where(UrlModel.full_url == full_url)
    response = await client.post("urls/shorten", json={"full_url": full_url})
    res = await test_session.execute(statement)
    assert response.json()["id"] == res.scalar_one().id


@pytest.mark.asyncio
async def test_redirect_url(client: AsyncClient):
    full_url = "https://www.google.com"
    response = await client.post("urls/shorten", json={"full_url": full_url})
    short_url = response.json()["id"]
    response = await client.get(f"urls/{short_url}")
    assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT
    assert response.headers["location"] == full_url


@pytest.mark.asyncio
async def test_url_clicks(test_session: AsyncSession, client: AsyncClient):
    full_url = "https://www.google.com"
    response = await client.post("urls/shorten", json={"full_url": full_url})
    short_url = response.json()["id"]
    statement = select(UrlModel).where(UrlModel.id == short_url)
    await client.get(f"urls/{short_url}")
    res = await test_session.execute(statement)
    assert res.scalar_one().clicks == 1


@pytest.mark.asyncio
async def test_get_url_status(client: AsyncClient):
    full_url = "https://www.google.com"
    response = await client.post("urls/shorten", json={"full_url": full_url})
    short_url = response.json()["id"]
    response = await client.get(f"urls/{short_url}/status")
    assert response.status_code == 200
    assert response.json() == {
        "id": short_url,
        "full_url": full_url,
        "clicks": 0,
        "is_taken_down": False,
    }


@pytest.mark.asyncio
async def test_delete_url(client: AsyncClient):
    full_url = "https://www.google.com"
    response = await client.post("urls/shorten", json={"full_url": full_url})
    short_url = response.json()["id"]
    response = await client.delete(f"urls/{short_url}")
    assert response.status_code == HTTPStatus.GONE
    assert response.json() == {"detail": "Gone"}


@pytest.mark.asyncio
async def test_url_is_taken_down(
        test_session: AsyncSession, client: AsyncClient
):
    full_url = "https://www.google.com"
    response = await client.post("urls/shorten", json={"full_url": full_url})
    short_url = response.json()["id"]
    await client.delete(f"urls/{short_url}")
    statement = select(UrlModel).where(UrlModel.id == short_url)
    res = await test_session.execute(statement)
    assert res.scalar_one().is_taken_down
