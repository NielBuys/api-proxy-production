# Dockerfile: Gist Proxy Service
# -----------------------------
# Base Image: Python 3.12 Slim (Debian Bookworm)
# - Provides a small, secure, and stable footprint.
# - Includes recent security patches.
#
# Security:
# - Runs as a non-privileged 'appuser' to minimize attack surface.
#
# Performance:
# - Utilizes Docker layer caching by copying requirements first.
# - Disables pip cache to keep image size small.

FROM python:3.12-slim-bookworm

# Create a system user to avoid running the application as root
RUN useradd -m appuser
USER appuser
WORKDIR /home/appuser

# Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/

# Port 8080 is common for Cloud Run/Azure App Service
EXPOSE 8080

# Execute the application using Uvicorn
# Using python -m uvicorn ensures the app module is in the path
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]