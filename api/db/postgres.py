import logging
import typing as t
from contextlib import asynccontextmanager

import asyncpg

from api.core.config import Config

# Connection pool will be created during the startup
db_pool: asyncpg.pool.Pool[asyncpg.Record] | None = None


async def init_db_pool(config: Config) -> asyncpg.Pool[asyncpg.Record]:
    """Initialize the asynchronous database connection pool."""
    global db_pool
    if db_pool is None:
        try:
            db_pool = await asyncpg.create_pool(
                user=config.postgres_user,
                password=config.postgres_password.get_secret_value(),
                database=config.postgres_db,
                host=config.postgres_host,
                port=config.postgres_port,
                min_size=1,
                max_size=10,
            )
        except Exception as e:
            logging.exception("Error creating the database pool")
            raise e from None
    return t.cast(asyncpg.Pool[asyncpg.Record], db_pool)


@asynccontextmanager
async def get_db(config: Config) -> t.AsyncGenerator[asyncpg.Connection, None]:
    """Context manager for managing PostgreSQL database connections."""
    connection: asyncpg.Connection | None = None
    global db_pool
    try:
        if db_pool is None:
            db_pool = await init_db_pool(config)
        connection = t.cast(asyncpg.Connection, await db_pool.acquire())
        yield connection
    except Exception as e:
        logging.exception("Database error")
        raise e from None
    finally:
        if connection:
            await t.cast(asyncpg.Pool[asyncpg.Record], db_pool).release(
                t.cast(asyncpg.pool.PoolConnectionProxy, connection)
            )
