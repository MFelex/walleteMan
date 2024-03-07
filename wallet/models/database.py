from typing import Iterator

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from wallet.core.config import env

engine = create_engine(str(env.DB_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

try:
    logger.info(f'Init Database from address: {env.DB_URL.hosts()[0].get("host")}')
except AttributeError:
    logger.error("Can not initialize Database")


def get_conn():
    engine.connect()
    return engine.url.database


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
