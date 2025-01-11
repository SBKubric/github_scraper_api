from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from datetime import date
import psycopg2
from psycopg2.extras import RealDictCursor
from ..core.config import Config

# Настройки для подключения к PostgreSQL
DB_CONFIG = {
    "dbname": Config.postgres_db,
    "user": Config.postgres_user,
    "password": Config.postgres_password.get_secret_value(),
    "host": Config.postgres_host,
    "port": Config.postgres_port,
}

def get_db_connection():
    """Подключение к базе данных PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def get_top_100_repositories(
    sort_by: Optional[str] = Query("stars", regex="^(repo|owner|stars|watchers|forks|open_issues|language)$"),
    order: Optional[str] = Query("desc", regex="^(asc|desc)$")
):
    """Получение топ-100 публичных репозиториев."""
    query = f"""
        SELECT repo, owner, position_cur, position_prev, stars, watchers, forks, open_issues, language
        FROM top100
        ORDER BY {sort_by} {order.upper()}
        LIMIT 100
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_repo_activity(
    owner: str,
    repo: str,
    since: Optional[date] = None,
    until: Optional[date] = None
):
    """Получение информации об активности репозитория по коммитам за выбранный промежуток времени."""
    base_query = """
        SELECT date, commits, authors
        FROM activity
        WHERE repo = %s AND owner = %s
    """
    conditions = []
    params = [repo, owner]
    
    if since:
        conditions.append("date >= %s")
        params.append(since)
    if until:
        conditions.append("date <= %s")
        params.append(until)
    
    if conditions:
        base_query += " AND " + " AND ".join(conditions)
    base_query += " ORDER BY date"
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(base_query, tuple(params))
                results = cursor.fetchall()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))