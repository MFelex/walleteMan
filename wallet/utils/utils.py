from loguru import logger

from wallet.models.database import get_conn


def is_db_available():
    try:
        db_conn = get_conn()
    except Exception as e:
        logger.exception(f"DB connection error {e.__cause__}")
        return "DB connection error!"
    else:
        return db_conn
