import logging

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    project_name: str = "ParserAPI"
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    uvicorn_host: str
    uvicorn_port: int


def get_settings() -> Config:
    try:
        return Config()  # type: ignore  # noqa: PGH003
    except Exception as e:
        logging.exception("Failed to initialize config!")
        raise e from None
