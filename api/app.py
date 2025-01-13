import logging
import typing as t
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from api.api.v1.routers import repositories
from api.core.config import get_settings
from api.core.logger import get_logger as logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> t.AsyncGenerator[None, None]:
    """
    Create and configure a FastAPI application instance.
    """
    logger()

    # Register middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production needs to be set to domain list
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    register_routers(app)
    logging.debug("Init")

    yield None

    logging.info("Shutting down FastAPI application")


def register_routers(app: FastAPI) -> None:
    """
    Register all application routers.
    """
    app.include_router(
        repositories.get_github_router(),
        tags=["Github", "repository"],
    )

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}


# Create app instance
app = FastAPI(
    title=get_settings().project_name,
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/docs.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
