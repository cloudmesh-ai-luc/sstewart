"""FastAPI application entry point.

This file creates the FastAPI app, registers the API routers and provides
simple health/readiness endpoints. The implementation is deliberately kept
lightweight and does not depend on any external services other than the
SQLAlchemy models defined in the project.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Import the routers that implement the required endpoints.
from .api.routes import messages


def create_app() -> FastAPI:
    """Create and configure a FastAPI application.

    Returns
    -------
    FastAPI
        The configured FastAPI instance.
    """
    app = FastAPI(title="911 Call Center Analysis API")

    # Register API routers under the ``/api`` prefix.
    app.include_router(messages.router, prefix="/api")

    # Simple health endpoints used by the deployment scripts.
    @app.get("/health", tags=["health"])
    async def health() -> JSONResponse:
        """Return a minimal health check response.

        The endpoint is deliberately tiny – it only confirms that the Python
        process is up and can respond to HTTP requests.
        """
        return JSONResponse(content={"status": "ok"})

    @app.get("/ready", tags=["health"])
    async def ready() -> JSONResponse:
        """Readiness probe.

        In a full production system this would verify that critical external
        dependencies (database, message broker, etc.) are reachable. For the
        purpose of this educational project we simply return ``ok`` – the
        database connection is validated lazily when the first request hits a
        CRUD endpoint.
        """
        return JSONResponse(content={"status": "ready"})

    return app


# The ``app`` variable is the convention used by ASGI servers such as ``uvicorn``.
app = create_app()
