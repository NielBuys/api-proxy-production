import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="GitHub Gist Proxy")

GITHUB_URL = "https://api.github.com/users/{username}/gists"


@app.get("/")
async def root():
    return {
        "message": "Welcome to my Gist API proxy! This API fetches public gists for a given GitHub username.",
        "instructions": "Please add a GitHub username to the URL, e.g., /nielbuys",
    }


@app.get("/{username}")
async def get_user_gists(username: str):
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
