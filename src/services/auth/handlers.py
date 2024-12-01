from typing import Optional

from guardpost import AuthenticationHandler, Identity

import api  # noqa: F401
import api.v1  # noqa: F401

from blacksheep import Request
from blacksheep.exceptions import BadRequest
from jwt import InvalidTokenError
from .utils import decode_jwt


class AuthHandler(AuthenticationHandler):
    async def authenticate(self, context: Request) -> Optional[Identity]:
        token = context.get_first_header(b"Authorization")
        if token:
            try:
                payload = decode_jwt(token.decode())
            except InvalidTokenError:
                raise BadRequest("Некорректный токен")
            context.identity = Identity(payload, "AUTHORIZATION")
        else:
            context.identity = None
        return context.identity
