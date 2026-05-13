"""
Unit and Integration Tests
--------------------------
This suite validates the FastAPI endpoints using httpx and pytest-asyncio.
It uses ASGITransport to mock the server environment, allowing for fast,
in-memory testing of the application logic.

Tests:
    - test_root_endpoint: Verifies the landing page content and status.
    - test_get_gists_structure: Ensures the API response follows the expected schema.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    """
    Test that the root (/) endpoint returns 200 OK and
    the correct instructional message.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert "Please add a GitHub username" in response.json()["instructions"]


@pytest.mark.asyncio
async def test_get_gists_structure():
    """
    Test that the /{username} endpoint returns the correct JSON keys
    and that the 'gists' field is a list.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # We use a real username here to ensure a valid 200 response
        response = await ac.get("/nielbuys")

    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "gists" in data
    assert isinstance(data["gists"], list)
