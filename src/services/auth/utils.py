from datetime import datetime, timedelta

import bcrypt
import jwt
from typing import Dict
from dataclasses import asdict


from config import settings
from services.auth.types import JwtPayload, UserAuthInfo


def encode_jwt(
    payload: JwtPayload,
    private_key: str = settings.PRIVATE_JWT_KEY,
    algorithm: str = settings.JWT_ALGORITHM,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    to_encode = asdict(payload)
    now = datetime.now()
    expire = now + timedelta(minutes=int(expire_minutes))
    to_encode.update(exp=expire, iat=now)
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded_jwt


def decode_jwt(
    token: str,
    key: str = settings.PUBLIC_JWT_KEY,
    algorithm: str = settings.JWT_ALGORITHM,
) -> Dict[str, str]:
    decoded_jwt = jwt.decode(token, key, algorithms=[algorithm])
    return decoded_jwt


def generate_user_token(user: UserAuthInfo) -> str:
    return encode_jwt(JwtPayload(id=str(user.id), email=user.email))


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    bytes_password: bytes = password.encode()
    return bcrypt.hashpw(bytes_password, salt)


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
