from typing import Optional, List

from blacksheep import get, patch
from guardpost import Identity

from services.auth.types import authenticated
from blacksheep.server.authorization import auth

from services.users import (
    get_user_info,
    UserInfo,
    UserUpdateInfo,
    update_user_info,
    find_users_by_substring,
)


@auth(authenticated)
@get("/api/v1/users/me")
async def user_info(user: Optional[Identity]) -> UserInfo:
    """
    Получение информации об авторизованном пользователе
    """
    return await get_user_info(user.get("id"))


@auth(authenticated)
@patch("/api/v1/users/me")
async def update_self_user(
    user: Optional[Identity], update_info: UserUpdateInfo
) -> UserInfo:
    """
    Обновление информации об авторизованном пользователе
    """
    await update_user_info(user.get("id"), update_info)
    return await get_user_info(user.get("id"))


@get("/api/v1/users/find/{substring}")
async def find_users(substring: str) -> List[UserInfo]:
    return await find_users_by_substring(substring)
