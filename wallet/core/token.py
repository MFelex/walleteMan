from datetime import datetime, timedelta
from typing import Union

from jose import jwt, constants, JWTError
from starlette import status
from pydantic import BaseModel, ConfigDict
from fastapi import Depends, HTTPException

from starlette.requests import Request

from wallet.core.config import Settings, get_env


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Could not validate request token',
    headers={'WWW-Authenticate': 'Bearer'},
)


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    email: str
    position: str
    first_name: str
    last_name: str
    phone_number: str


def get_user_token(
        request: Request,
        env: Settings = Depends(get_env),
) -> Union[Token, Exception]:
    authorization: str = request.headers.get('authorization', '')

    if not (authorization and len(authorization.split()) == 2):
        raise forbidden_exception

    token_type = authorization.split()[0].upper()
    if token_type != 'BEARER':
        raise forbidden_exception

    try:
        key = env.JWT_PUBKEY
        tkn = authorization.split()[1]
        payload = jwt.decode(tkn, key, algorithms=[constants.ALGORITHMS.ES256, ])

    except JWTError:
        raise credentials_exception

    if not payload:
        raise credentials_exception

    return Token(
        email=payload['email'],
        user_id=payload['user_id'],
        position=payload['position'],
        last_name=payload['last_name'],
        first_name=payload['first_name'],
        phone_number=payload['phone_number'],
    )


def make_token(_type: str, expire: int, data: Token, env: Settings) -> str:
    payload = {
        'type': _type,
        'sub': data.user_id,
        'email': data.email,
        'user_id': data.user_id,
        'position': data.position,
        'last_name': data.last_name,
        'first_name': data.first_name,
        'phone_number': data.phone_number,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=expire)
    }
    token = jwt.encode(payload, env.JWT_PVTKEY, 'ES256')
    return token
