from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Extra  # noqa


class Settings(BaseSettings):
    DEBUG: bool
    ORIGIN: str

    DB_URL: PostgresDsn

    JWT_PUBKEY: str
    JWT_PVTKEY: str
    JWT_ACCESS_EXPIRE: int
    JWT_REFRESH_EXPIRE: int

    class Config:
        env_file = ".env"
        extra = Extra.ignore


@lru_cache()
def get_env():
    return Settings()


env = get_env()
