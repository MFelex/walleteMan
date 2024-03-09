from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator


class WalletView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: int
    user_id: int
    blocked_amount: int
    created_at: datetime

    @field_validator('created_at')  # noqa
    @classmethod
    def convert_time_to_string(cls, v: datetime) -> str:
        return v.isoformat()


class Deposit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tx_id: str
    amount: int
    user_id: int

    @field_validator('amount')  # noqa
    @classmethod
    def negetive_amount(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('negative amount')
        return v


class WithdrawRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: int
    user_id: int
    withdraw_at: datetime


    @field_validator('withdraw_at')  # noqa
    @classmethod
    def check_now(cls, v: datetime) -> datetime:
        if v < datetime.now(timezone.utc):
            raise ValueError('Time has expired')
        return v


class WithdrawAction(BaseModel):
    id: int
    user_id: int
