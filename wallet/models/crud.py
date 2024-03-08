from datetime import datetime
from typing import Union, List

from sqlalchemy import asc
from sqlalchemy.orm import Session

from wallet.models.choices import WithdrawStatus
from wallet.models.dbmodels import Wallet, Deposit, Withdraw
from wallet.models.schemas import Deposit, WithdrawRequest


def create_wallet(user_id: int, db: Session) -> Wallet:
    wlt = Wallet(user_id=user_id)
    db.add(wlt)
    db.commit()
    return wlt


def get_wallet(pk: int, db: Session) -> Union[Wallet, None]:
    return db.query(Wallet).filter(Wallet.id == pk).first()  # noqa


def get_wallet_by_user_id(user_id: int, db: Session) -> Union[Wallet, None]:
    return db.query(Wallet).filter(Wallet.user_id == user_id).first()  # noqa


def get_with_lock_wallet(user_id: int, db: Session) -> Union[Wallet, None]:
    return db.query(Wallet).filter(Wallet.user_id == user_id).with_for_update().first()  # noqa


def create_deposit(body: Deposit, db: Session) -> None:
    trx = Deposit(**body.model_dump())
    db.add(trx)
    db.commit()


def create_withdraw(body: WithdrawRequest, db: Session) -> None:
    wit = Withdraw(**body.model_dump())
    db.add(wit)
    db.commit()


def get_withdraw(pk: int, db: Session) -> Union[Withdraw]:
    return db.query(Withdraw).filter(Withdraw.id == pk).first()  # noqa


def get_open_withdraw_requests(db: Session) -> List[Withdraw]:
    return db.query(Withdraw).filter(  # noqa
        Withdraw.status == WithdrawStatus.OPEN,
        Withdraw.withdraw_at <= datetime.now(),  # noqa
    ).order_by(
        asc(Withdraw.withdraw_at)  # noqa
    ).all()


def set_failed_withdraw(withdraw: Withdraw, description: str, db: Session) -> None:
    withdraw.status = WithdrawStatus.FAILED
    withdraw.description = description
    db.add(withdraw)
    db.commit()


def set_pending_withdraw(withdraw: Withdraw, db: Session) -> None:
    withdraw.status = WithdrawStatus.PENDING
    db.add(withdraw)
    db.commit()
