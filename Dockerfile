FROM ubuntu:26.04

# Prevent interactive prompts during apt operations
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv build-essential git netcat curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only the files needed for installing dependencies first (helps Docker cache)
COPY pyproject.toml pyproject.toml
COPY requirements.txt requirements.txt
COPY src ./src
COPY Makefile Makefile
COPY README.md README.md

# Upgrade pip and install python dependencies
RUN pip3 install --upgrade pip && \
    if [ -f requirements.txt ]; then pip3 install -r requirements.txt; else pip3 install .; fi

# Expose the port the FastAPI app runs on
EXPOSE 8000

# Health‑check that queries the FastAPI health endpoint
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:${FASTAPI_PORT:-8000}/health || exit 1

# Entrypoint script waits for the database to become reachable before starting
# the application. The script is added later in this Dockerfile.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
