# Gist Proxy API - Solution Documentation

This solution provides a FastAPI-based web server that proxies GitHub Gist data. 
It has been containerized and includes automated testing, linting, and publishing to the GitHub Container Registry (GHCR).

*Note: Comments have been added to all source files to assist with the review process.*

## 1. How to Run

### 1.1 Using GHCR (Recommended)
This method utilizes the pre-built image from the CI pipeline.
1. **Pull:** `docker pull ghcr.io/equalexperts-assignments/equal-experts-dominant-philosophical-comfortable-collaboration-0e45fb350e09:latest`
2. **Run:** `docker run -p 8080:8080 ghcr.io/equalexperts-assignments/equal-experts-dominant-philosophical-comfortable-collaboration-0e45fb350e09:latest`
3. **Test:** Navigate to `http://localhost:8080/octocat`

### 1.2 Using Local Docker
Use this to build the image from source on your local machine.
1. **Build:** `docker build -t gist-proxy .`
2. **Run:** `docker run -p 8080:8080 gist-proxy`
3. **Test:** Navigate to `http://localhost:8080/octocat`

### 1.3 Using Local Python
1. **Install:** `pip install -r requirements.txt`
2. **Run:** `python -m uvicorn app.main:app --port 8080`

## 2. Automated Testing
Tests are written using `pytest` and `httpx`.
- **Run locally:** `pytest`
- **CI/CD:** Tests are automatically executed on every push via GitHub Actions.

## 3. Design Decisions & Operability
- **Security:** The Docker container runs as a non-root `appuser` for improved security posture.
- **Linting:** Ruff is used to ensure PEP 8 compliance and code quality.
- **Observability:** - Standardized logging to `stdout` for container log aggregation.
    - Monitoring: I've included example configurations for New Relic in the Dockerfile (currently commented out).
- **Asynchronous:** Built using `FastAPI` and `httpx` for non-blocking I/O when fetching from GitHub.

## 4. GitHub Actions Workflows
- **Linting:** Runs on every PR to ensure style consistency.
- **Testing:** Validates the API logic before merging.
- **Build & Publish:** Validates the Docker build and pushes the `:latest` and `:sha` tags to GHCR upon merging to the `solution` branch.