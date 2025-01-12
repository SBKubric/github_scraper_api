from pydantic import BaseSettings, SecretStr


class Config(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    uvicorn_host: str
    uvicorn_port: int
