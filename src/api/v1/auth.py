from blacksheep import post

from api.exceptions import UserAlreadyExistsException
from services.auth.login import register_user
from services.auth.types import UserAuthInfo, RegisterUser


@post("/api/v1/auth/register")
async def register_new_user(user: RegisterUser) -> UserAuthInfo:
    new_user = await register_user(user)
    return new_user.unwrap_or_raise(UserAlreadyExistsException)
