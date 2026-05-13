"""
Main Application Module
-----------------------
This module defines a FastAPI web service that acts as a proxy for the GitHub Gist API.
It allows users to retrieve a list of public Gist URLs for any valid GitHub username.

Usage:
    - GET /: Returns a welcome message and instructions.
    - GET /{username}: Returns a JSON object containing the username and a list of their Gist URLs.

Deployment:
    Designed for deployment on Azure App Service and local Docker environments.
"""

import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="GitHub Gist Proxy")

GITHUB_URL = "https://api.github.com/users/{username}/gists"


@app.get("/")
async def root():
    """Returns the entry point message for the API."""
    return {
        "message": "Welcome to my Gist API proxy! This API fetches public gists for a given GitHub username.",
        "instructions": "Please add a GitHub username to the URL, e.g., /nielbuys",
    }


@app.get("/{username}")
async def get_user_gists(username: str):
    """
    Fetches public gists for a specific GitHub user.

    Args:
        username (str): The GitHub handle to query.

    Returns:
        dict: A collection of URLs pointing to the user's gists.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(GITHUB_URL.format(username=username))

            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="GitHub User not found")

            response.raise_for_status()
            data = response.json()

            return {
                "username": username,
                "gists": [gist.get("html_url") for gist in data],
            }

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail="GitHub API Error"
            )
