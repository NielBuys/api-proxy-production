# GitHub Gist Proxy API

This repository contains a lightweight, containerized FastAPI web server that acts as a proxy for the GitHub Gist API. 

I put this project together during a personal coding session to build a clean, production-ready implementation of an API proxy. It fetches a specified user's public Gists, includes automated testing, incorporates a CI/CD pipeline, and supports both Docker and Kubernetes deployments.

---

## 🚀 Getting Started & How to Run

The application listens for requests on port `8080`. You can test the endpoint by requesting public data for any GitHub user (e.g., `octocat`) at `http://localhost:8080/octocat`.

Choose one of the four methods below to get the application up and running:

### 1. Running via Pre-built Container (Recommended)
You can pull and run the pre-built image directly from the GitHub Container Registry without needing the source code:

```bash
# Pull the specific image version
docker pull ghcr.io/nielbuys/assignment:sha-8794645

# Run the container mapping host port 8080 to container port 8080
docker run -p 8080:8080 ghcr.io/nielbuys/assignment:sha-8794645
```

### 2. Running via Local Docker Build
If you want to build the Docker image locally from the source code repository:

```bash
# Build the Docker image from the local Dockerfile
docker build -t gist-proxy .

# Run the newly built container
docker run -p 8080:8080 gist-proxy
```

### 3. Running Locally with Python
To run the application directly on your host machine without using any containerization tools:

```bash
# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Uvicorn ASGI server
python -m uvicorn app.main:app --port 8080
```

### 4. Deploying to Kubernetes
Ensure your local Kubernetes cluster is running (e.g., via Docker Desktop or Minikube) before applying the manifests:

```bash
# Verify your local cluster status
kubectl config current-context
kubectl get nodes

# Deploy the application pod/deployment setup
kubectl apply -f deployment.yaml

# Open a temporary network tunnel to access the application at http://localhost:8080
kubectl port-forward deployment/gist-api-deployment 8080:8080

# (Optional) Apply the service manifest for permanent internal network routing
kubectl apply -f service.yaml
```

## Testing & Code Quality

### Running the Test Suite
Tests are written using pytest and httpx. You can run them locally in two ways:

### Using local Python environment:

```bash
pip install -r requirements.txt
pytest
```

### Using Docker (Ephemeral Test Environment):
If you want to ensure your tests run in an isolated environment without local dependencies:

```bash
docker build --target test -t gist-proxy-tests .
```

### Code Formatting & Linting
This project leverages Ruff for fast Python linting and code formatting:

```bash
# Check code for style errors and apply safe auto-fixes
ruff check --fix

# Format code layout and sort imports
ruff format
```

## Design Decisions & Operability

- Asynchronous I/O: Built using FastAPI and httpx to ensure non-blocking network calls when fetching data from GitHub's upstream API.
- Security & Hardening: The Dockerfile is optimized to run as a non-root appuser rather than default root, adhering to security best practices.
- Code Quality: Integrated Ruff for modern, high-performance linting and PEP 8 compliance.
- Observability: * Configured standardized logging to stdout for seamless container log aggregation.
Added placeholder/example configurations for New Relic APM tracking inside the Dockerfile (currently commented out).

## GitHub Actions Workflow
The repository includes automation workflows to simulate a real-world engineering pipeline:

1. Linting: Validates code quality and formatting on every pull request.
2. Testing: Automatically runs the test suite to ensure structural integrity before code shifts.
3. Build & Publish: Builds the Docker container and pushes tagged versions (:latest and :sha-*) directly to the GitHub Container Registry (GHCR).