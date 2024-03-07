from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError  # noqa

from wallet import __version__
from wallet.core.errors import ok
from wallet.utils.utils import is_db_available
from wallet.controller.wallet import route as wallet_route


route = APIRouter()
route.include_router(wallet_route, prefix='/wallet', tags=['wallet'])


@route.get("/status/")
def home():
    db_conn: Session = is_db_available()

    return ok({"version": __version__, "database": db_conn})
