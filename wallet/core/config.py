from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Extra  # noqa


class Settings(BaseSettings):
    DEBUG: bool
    ORIGIN: str

    DB_URL: PostgresDsn
    BROKER_URL: str

    JWT_PUBKEY: str
    JWT_PVTKEY: str  # noqa
    JWT_ACCESS_EXPIRE: int
    JWT_REFRESH_EXPIRE: int

    WITHDRAW_BEAT_SECOND: int

    THIRD_PARTY_SERVICE_URL: str

    class Config:
        env_file = ".env"
        extra = Extra.ignore


@lru_cache()
def get_env():
    return Settings()


env = get_env()
