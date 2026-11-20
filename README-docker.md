# Docker Development Setup for the 911 Call Center Analysis API

This repository contains a FastAPI backend that can be run locally or inside
Docker containers. The Docker setup uses **Ubuntu 26.04** as the base image and
includes a **docker‑compose.yml** that brings up two services:

* **mariadb** – a MariaDB database (image `mariadb:11.4`).
* **api** – the FastAPI application built from the local source code.

## Prerequisites

* Docker Engine (or Docker Desktop) >= 27.0
* Docker Compose (the `docker compose` CLI is bundled with newer Docker versions)
* (Optional) The environment variables required by the database. The easiest way
  to provide them is to create a `.env` file in the repository root. Example:

```
MARIADB_DATABASE=analysis
MARIADB_USER=analysis_user
MARIADB_PASSWORD=super_secret_password
MARIADB_ROOT_PASSWORD=another_secret_root_pw
# Port can be left as the default 3306
# MARIADB_PORT=3306
```

> **Note**: The `Config` class in `src/backend/app/services/config.py` expects the
> MariaDB passwords to be replaced from the placeholder values. The `.env`
> file above satisfies that requirement.

## Building & Running the Services

Two convenient `make` targets are provided:

* **`make start`** – builds the Docker image (if needed) and starts the services
  in detached mode.
* **`make stop`** – stops the containers and removes the network.

```bash
# Start everything
make start

# Stop everything
make stop
```

The `api` container maps port **8000** to the host, so you can reach the API at
`http://localhost:8000`. Example health‑check endpoint:

```bash
curl http://localhost:8000/health
# => {"status": "ok"}
```

## Inspecting Logs

If you need to view the logs of a specific service, you can use the standard
Docker Compose command:

```bash
docker compose logs -f api        # Follow API logs
docker compose logs -f mariadb    # Follow DB logs
```

## Rebuilding the Image

When you change Python dependencies or the Dockerfile, rebuild the image with:

```bash
docker compose build api
```

## Cleaning Up

To remove all containers, networks, and the named volume for MariaDB data:

```bash
make stop          # Stops the containers
docker volume rm $(docker volume ls -qf name=mariadb_data)
```

## Additional Make Targets

The root `Makefile` already contains many useful targets for development (e.g.
`make run` to start the FastAPI server locally, `make doc` to build the MkDocs
documentation, etc.). The Docker‑specific targets are added alongside those.

---

Happy coding! 🚑
