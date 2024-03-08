import json

import requests
from loguru import logger

from wallet.models.crud import *
from wallet.core.config import env
from wallet.task_manager import app
from wallet.models.database import db_session
from wallet.models.choices import WithdrawStatus
from wallet.models.schemas import WithdrawAction
from wallet.models.dbmodels import Withdraw, Wallet


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(env.WITHDRAW_BEAT_SECOND, withdraw_reqeust.s(), name='withdraw_beat')


@app.task(name='withdraw.request')
def withdraw_reqeust():
    # PLEASE RUN IT JUST WITH ONE WORKER
    db: Session = db_session
    withdraws: List[Withdraw] = get_open_withdraw_requests(db)
    if not withdraws:
        return 'No action'

    for withdraw in withdraws:
        user_id: int = withdraw.user_id
        wlt: Wallet = get_wallet_by_user_id(user_id, db)
        if not wlt:
            logger.error(f'User {user_id} has no wallet, please check withdraw scenario')
            description = 'User has now wallet'
            set_failed_withdraw(withdraw, description, db)
            return 'No Wallet'

        set_pending_withdraw(withdraw, db)

        wit = WithdrawAction(id=withdraw.id, user_id=user_id)
        withdraw_action.apply_async(kwargs={'data': wit.model_dump_json()})

    return f'Processed {len(withdraws)} requests'


@app.task(name='withdraw.action')
def withdraw_action(data):
    db: Session = db_session

    wit = WithdrawAction(**json.loads(data))
    withdraw: Withdraw = get_withdraw(wit.withdraw_id, db)
    wlt: Wallet = get_with_lock_wallet(wit.user_id, db)

    if wlt.amount < withdraw.amount:
        return f'insufficient balance of user {wit.user_id}'

    wlt.amount -= withdraw.amount
    wlt.blocked_amount += withdraw.amount
    db.add(wlt)
    db.commit()

    is_success, desc = withdraw_commit()
    if not is_success:
        wlt.blocked_amount -= withdraw.amount
        wlt.amount += withdraw.amount
        withdraw.status = WithdrawStatus.FAILED
        withdraw.description = desc

    else:
        wlt.blocked_amount -= withdraw.amount
        withdraw.status = WithdrawStatus.DONE

    db.add(wlt)
    db.add(withdraw)
    db.commit()

    return True


def withdraw_commit() -> (bool, str):
    is_success: bool = False
    status: str = ''

    url: str = env.THIRD_PARTY_SERVICE_URL
    try:
        res = requests.post(url, timeout=60)
        res.raise_for_status()
        status: int = int(res.json()['status'])

        if 200 <= status < 300:
            is_success = True

    except requests.HTTPError as e:
        logger.exception(e)
        status = e.response.text

    except requests.RequestException as e:
        logger.exception(e)
        status = e.__str__()

    return is_success, status
