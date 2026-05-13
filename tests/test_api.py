import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert "Please add a GitHub username" in response.json()["instructions"]


@pytest.mark.asyncio
async def test_get_gists_structure():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/nielbuys")

    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "gists" in data
    assert isinstance(data["gists"], list)
