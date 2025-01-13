import logging

from asyncpg import Connection as connection
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.core.config import get_settings
from api.db import get_db
from api.handlers import repositories as handlers
from api.models import Error, Repository, RepositoryActivity

router = APIRouter()
router.prefix = "/api/v1"


@router.get(
    "/github/top100",
    response_model=list[Repository],
    summary="Fetch Top 100 Repositories",
    description=(
        "Retrieve a list of the top 100 public repositories sorted by specified fields and order. "
        "Valid fields include repo, owner, stars, watchers, forks, open_issues, and language."
    ),
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": Error,
            "description": "Invalid sorting or ordering parameters.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Error,
            "description": "Database query failed.",
        },
    },
)
async def get_top_100_repositories(
    sort_by: str | None = Query(
        "stars", description="Sort by this field.", regex="^(repo|owner|stars|watchers|forks|open_issues|language)$"
    ),
    order: str | None = Query("desc", description="Sorting order (asc/desc).", regex="^(asc|desc)$"),
    db: connection = Depends(get_db(Depends(get_settings))),  # noqa: B008
) -> list[Repository]:
    try:
        if sort_by is None:
            sort_by = "repo"
        if order is None:
            order = "asc"
        return await handlers.get_top_100_repositories(sort_by, order, db)
    except Exception as e:
        logging.exception("Error fetching top 100 repositories")
        raise HTTPException(status_code=500, detail="Database query failed.") from e


@router.get(
    "/github/activity",
    response_model=list[RepositoryActivity],
    summary="Fetch Repository Activity",
    description="Retrieve activity data for a specific repository within an optional date range.",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": Error,
            "description": "Invalid query parameters.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": Error,
            "description": "Database query failed.",
        },
    },
)
async def get_repo_activity(
    owner: str,
    repo: str,
    since: str | None = Query(None, description="Filter by start date (YYYY-MM-DD)."),
    until: str | None = Query(None, description="Filter by end date (YYYY-MM-DD)."),
    db: connection = Depends(get_db(Depends(get_settings))),  # noqa: B008
) -> list[RepositoryActivity]:
    try:
        return await handlers.get_repo_activity(repo, owner, since, until, db)
    except Exception as e:
        logging.exception(f"Error fetching activity for {owner}/{repo}")
        raise HTTPException(status_code=500, detail="Database query failed.") from e


def get_github_router() -> APIRouter:
    return router
