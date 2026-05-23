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

import logging
from urllib import response
import httpx
from fastapi import FastAPI, HTTPException

# --- Logging Configuration ---
# Standardizes logs to show time, level, and message.
# In Docker/Azure, these are automatically collected from stdout.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("gist-proxy")

app = FastAPI(title="GitHub Gist Proxy")

GITHUB_URL = "https://api.github.com/users/{username}/gists"


@app.get("/")
async def root():
    """Returns the entry point message for the API."""
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to my Gist API proxy! This API fetches public gists for a given GitHub username.",
        "instructions": "Please add a GitHub username to the URL, e.g., /octocat",
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
    logger.info(f"Fetching gists for user: {username}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(GITHUB_URL.format(username=username))

            # Let raise_for_status() handle ALL error status codes (404, 403, 500, etc.)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Successfully retrieved {len(data)} gists for {username}")

            return {
                "username": username,
                "gists": [gist.get("html_url") for gist in data],
            }

        except httpx.HTTPStatusError as e:
            logger.error(
                f"GitHub API error for {username}: Status {e.response.status_code}"
            )
            
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=404, 
                    detail="GitHub User not found"
                )
            
            # For all other errors (403, 429, 500, etc.)
            raise HTTPException(
                status_code=e.response.status_code, 
                detail="GitHub API Error"
            )

        except Exception as e:
            logger.critical(f"Unexpected system error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")