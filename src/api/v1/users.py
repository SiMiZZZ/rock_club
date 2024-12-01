from typing import Optional

from blacksheep import get
from guardpost import Identity

from services.auth.types import authenticated
from blacksheep.server.authorization import auth

from services.users import get_user_info, UserInfo


@auth(authenticated)
@get("/api/v1/users/info")
async def user_info(user: Optional[Identity]) -> UserInfo:
    return await get_user_info(user.get("id"))
