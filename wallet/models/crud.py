from sqlalchemy.orm import Session

from wallet.models.dbmodels import Wallet, Deposit, Withdraw
from wallet.models.schemas import Deposit, WithdrawRequest


def create_wallet(user_id: int, db: Session) -> Wallet:
    wlt = Wallet(user_id=user_id)
    db.add(wlt)
    db.commit()
    return wlt


def get_wallet(pk: int, db: Session) -> Wallet:
    return db.query(Wallet).filter(Wallet.id == pk).first()  # noqa


def create_deposit(body: Deposit, db: Session) -> None:
    trx = Deposit(**body.model_dump())
    db.add(trx)
    db.commit()


def create_withdraw(body: WithdrawRequest, db: Session) -> None:
    wit = Withdraw(**body.model_dump())
    db.add(wit)
    db.commit()
