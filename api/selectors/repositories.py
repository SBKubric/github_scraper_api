import typing as t

import asyncpg


async def fetch_top_100_repositories(sort_by: str, order: str, db: asyncpg.Connection) -> list[dict[str, t.Any]]:
    """Database query to fetch top 100 repositories."""

    # sort_by and order should be already validated in handlers/repositories.py
    query = f"""
        SELECT repo, owner, position_cur, position_prev, stars, watchers, forks, open_issues, language
        FROM top100
        ORDER BY {sort_by} {order}
        LIMIT 100
    """  # noqa: S608
    result = await db.fetch(query)
    return result


async def fetch_repo_activity(
    repo: str,
    owner: str,
    db: asyncpg.Connection,
    since: str | None = None,
    until: str | None = None,
) -> list[dict[str, t.Any]]:
    """Database query to fetch repository activity."""
    base_query = """
        SELECT date, commits, authors
        FROM activity
        WHERE repo = $1 AND owner = $2
    """
    conditions = []
    params = [repo, owner]

    if since:
        conditions.append("date >= $3")
        params.append(since)
    if until:
        conditions.append("date <= $4")
        params.append(until)

    if conditions:
        base_query += " AND " + " AND ".join(conditions)
    base_query += " ORDER BY date"

    result = await db.fetch(base_query, *params)
    return result
