from asyncpg import Connection as connection

from api.core import exceptions as exc
from api.models import Repository, RepositoryActivity
from api.selectors import repositories as do_select

VALID_SORT_FIELDS = {"repo", "owner", "stars", "watchers", "forks", "open_issues", "language"}
VALID_ORDER = {"asc", "desc"}


async def get_top_100_repositories(sort_by: str, order: str, db: connection) -> list[Repository]:
    """Business logic to fetch top 100 repositories."""
    if sort_by not in VALID_SORT_FIELDS or order not in VALID_ORDER:
        raise exc.ValidationException(  # noqa: TRY003
            f"Invalid 'sort_by' or 'order' value. Must be one of {VALID_SORT_FIELDS} or {VALID_ORDER}.",
        )
    return [Repository(**rec) for rec in await do_select.fetch_top_100_repositories(sort_by, order, db)]


async def get_repo_activity(
    repo: str, owner: str, since: str | None, until: str | None, db: connection
) -> list[RepositoryActivity]:
    """Business logic to fetch repository activity."""
    return [RepositoryActivity(**rec) for rec in await do_select.fetch_repo_activity(repo, owner, db, since, until)]
