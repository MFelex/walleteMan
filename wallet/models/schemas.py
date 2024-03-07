from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WalletView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: str
    user_id: int
    blocked_amount: str
    created_at: datetime

    @field_validator('created_at')  # noqa
    @classmethod
    def convert_string(cls, v: datetime) -> str:
        return v.isoformat()


class Deposit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tx_id: str
    amount: str
    user_id: str


class WithdrawRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: str
    user_id: str
    withdraw_at: datetime


    @field_validator('withdraw_at')  # noqa
    @classmethod
    def check_now(cls, v: datetime) -> datetime:
        if v < datetime.now():
            raise ValueError('Time has expired')
        return v
