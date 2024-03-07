from sqlalchemy import func, BigInteger, Numeric
from sqlalchemy import Column, Integer, String, DateTime, Enum

from wallet.models.choices import WithdrawStatus
from wallet.models.database import Base


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Wallet(BaseModel):
    __tablename__ = 'wallet'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, index=True)
    user_id = Column(BigInteger().with_variant(Integer, 'sqlite'), index=True, unique=True, nullable=False)
    amount = Column(Numeric(precision=50, scale=10), default='0')
    blocked_amount = Column(Numeric(precision=50, scale=10), default='0')


class Deposit(BaseModel):
    __tablename__ = 'deposit'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, index=True)
    user_id = Column(BigInteger().with_variant(Integer, 'sqlite'), index=True, nullable=False)
    amount = Column(Numeric(precision=50, scale=10), default='0')
    tx_id = Column(String, unique=True, nullable=False)
    updated_at = None


class Withdraw(BaseModel):
    __tablename__ = 'withdraw'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, index=True)
    user_id = Column(BigInteger().with_variant(Integer, 'sqlite'), index=True, nullable=False)
    amount = Column(Numeric(precision=50, scale=10), default='0')
    status = Column(Enum(WithdrawStatus), default=WithdrawStatus.OPEN)
    withdraw_at = Column(DateTime(timezone=True), nullable=False)
    description = Column(String, nullable=True)
