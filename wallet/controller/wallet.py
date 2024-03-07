from loguru import logger
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from wallet.models.database import get_db
from wallet.models.schemas import Deposit, WithdrawRequest
from wallet.core.errors import created, ok
from wallet.services import wallet as service
from wallet.core.exceptions import CustomException

route = APIRouter()


@route.post('/{user_id}/')
def create_wallet(user_id: int, db: Session = Depends(get_db)):
    logger.info(f'Create user wallet of user_id {user_id}')
    try:
        res = service.create_wallet(user_id, db)
    except CustomException as e:
        logger.exception(e)
        return e.http_response()
    return created(res)


@route.get('/{pk}/')
def get_wallet(pk: int, db: Session = Depends(get_db)):
    logger.info(f'Get user wallet of id {pk}')
    try:
        res = service.get_wallet(pk, db)
    except CustomException as e:
        logger.exception(e)
        return e.http_response()
    return ok(res)


@route.post('/deposit/')
def deposit(body: Deposit, db: Session = Depends(get_db)):
    logger.info(f'Deposit transaction {body.model_dump()}')
    try:
        res = service.deposit(body, db)
    except CustomException as e:
        logger.exception(e)
        return e.http_response()
    return created(res)


@route.post('/withdraw/request/')
def withdraw_request(body: WithdrawRequest, db: Session = Depends(get_db)):
    logger.info(f'Withdraw request {body.model_dump()}')
    try:
        res = service.withdraw_request(body, db)
    except CustomException as e:
        logger.exception(e)
        return e.http_response()
    return created(res)
