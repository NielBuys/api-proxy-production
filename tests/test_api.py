"""
Unit Tests for Gist Proxy API
-----------------------------
Uses mocking to avoid calling the real GitHub API.
"""

import pytest
from httpx import AsyncClient, ASGITransport, Response
import respx
from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test the root endpoint - no external dependencies."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "Welcome to my Gist API proxy" in data["message"]
    assert "Please add a GitHub username" in data["instructions"]


@respx.mock
@pytest.mark.asyncio
async def test_get_gists_success():
    """Test successful case with mocked GitHub response."""
    # Mock the GitHub API call
    mock_gists = [
        {"html_url": "https://gist.github.com/octocat/12345"},
        {"html_url": "https://gist.github.com/octocat/67890"}
    ]

    respx.get("https://api.github.com/users/octocat/gists").mock(
        return_value=Response(200, json=mock_gists)
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/octocat")

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "octocat"
    assert len(data["gists"]) == 2
    assert "https://gist.github.com/octocat/12345" in data["gists"]


@respx.mock
@pytest.mark.asyncio
async def test_user_not_found():
    """Test 404 handling from GitHub."""
    respx.get("https://api.github.com/users/unknownuser/gists").mock(
        return_value=Response(404, json={"message": "Not Found"})
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/unknownuser")

    assert response.status_code == 404
    assert response.json()["detail"] == "GitHub User not found"