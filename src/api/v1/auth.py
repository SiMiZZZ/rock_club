from blacksheep import post

from api.exceptions import UserAlreadyExistsException, InvalidAuthDataException
from services.auth.login import register_user, login_user
from services.auth.types import UserAuthInfo, RegisterUser, LoginUser


@post("/api/v1/auth/register")
async def register_new_user(user_data: RegisterUser) -> UserAuthInfo:
    """
    Регистрация пользователя
    """
    user = await register_user(user_data)
    return user.unwrap_or_raise(UserAlreadyExistsException)


@post("/api/v1/auth/login")
async def auth_user(user_data: LoginUser) -> UserAuthInfo:
    """
    Авторизация пользователя
    """
    user = await login_user(user_data)
    return user.unwrap_or_raise(InvalidAuthDataException)
