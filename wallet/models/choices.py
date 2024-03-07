import enum


class WithdrawStatus(str, enum.Enum):
    OPEN = 'OPEN'
    PENDING = 'PENDING'
    DONE = 'DONE'
    FAILED = 'FAILED'
