from typing import Optional

from guardpost import AuthenticationHandler, Identity

import api  # noqa: F401
import api.v1  # noqa: F401

from blacksheep import Request
from blacksheep.exceptions import BadRequest
from jwt import InvalidTokenError

from .types import authenticated
from .utils import decode_jwt


class AuthHandler(AuthenticationHandler):
    async def authenticate(self, context: Request) -> Optional[Identity]:
        token = context.get_first_header(b"Authorization")
        print(token)
        if token:
            try:
                payload = decode_jwt(token.decode())
                print(payload)
            except InvalidTokenError:
                raise BadRequest("Некорректный токен")
            context.identity = UserData(payload, authenticated)
            print(context.identity.claims)
        else:
            context.identity = None
        return context.identity


class UserData(Identity):
    @property
    def id(self) -> Optional[str]:
        return self.get("id") or self.sub

    @property
    def name(self) -> Optional[str]:
        return self.get("name")

    @property
    def email(self) -> Optional[str]:
        return self.get("email")

    @property
    def role(self) -> Optional[str]:
        return self.get("role")
