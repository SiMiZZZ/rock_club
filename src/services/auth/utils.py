import random
import string
from datetime import datetime, timedelta

import bcrypt
import jwt
from typing import Dict
from dataclasses import asdict


from config import settings
from services.auth.types import JwtPayload


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


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    bytes_password: bytes = password.encode()
    return bcrypt.hashpw(bytes_password, salt)


def generate_password():
    password = ""
    alphabet = string.ascii_letters + string.digits
    for a in range(10):
        password += random.choice(alphabet)
    return password
