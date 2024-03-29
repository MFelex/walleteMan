from typing import Dict

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from wallet.models import crud
from wallet.models.crud import get_wallet_by_user_id, charge_wallet
from wallet.models.dbmodels import Wallet
from wallet.models.schemas import WalletView, Deposit, WithdrawRequest
from wallet.core.exceptions import BadRequestException, NotFoundException


def create_wallet(user_id: int, db: Session) -> Dict:
    try:
        wlt: Wallet = crud.create_wallet(user_id, db)
    except IntegrityError as e:
        logger.warning(f'user wallet of {user_id} already exist {e}')
        raise BadRequestException('Already exist')

    return WalletView.model_validate(wlt).model_dump()


def get_wallet(pk: int, db: Session) -> Dict:
    wlt: Wallet = crud.get_wallet(pk, db)
    if not wlt:
        logger.warning(f'Wallet of ID {pk} not found')
        raise NotFoundException('There is no wallet')

    return WalletView.model_validate(wlt).model_dump()


def deposit(body: Deposit, db: Session) -> str:
    wlt: Wallet = crud.get_wallet_by_user_id(body.user_id, db)
    if not wlt:
        wlt: Wallet = crud.create_wallet(body.user_id, db)

    try:
        crud.create_deposit(body, db)
    except IntegrityError as e:
        logger.error(f'Deposit transaction of {body.tx_id} already exist {e}')
        raise BadRequestException('Duplicated transaction')

    charge_wallet(wlt, body.amount, db)

    return 'Successfully charged'


def withdraw_request(body: WithdrawRequest, db: Session) -> str:
    if not get_wallet_by_user_id(body.user_id, db):
        raise BadRequestException('First, make a wallet')

    crud.create_withdraw(body, db)
    return f'The withdrawal was set for {str(body.withdraw_at)}'
