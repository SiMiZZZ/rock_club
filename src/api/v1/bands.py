from typing import Optional, List

from blacksheep import post, get
from guardpost import Identity

from services.auth.types import authenticated
from blacksheep.server.authorization import auth

from services.bands import create_band, BandCreate, get_user_groups, BandShortInfo


@auth(authenticated)
@post("/api/v1/bands")
async def create_new_band(user: Optional[Identity], band: BandCreate) -> BandShortInfo:
    """
    Создание новой группы
    """
    return await create_band(user.get("id"), band)


@auth(authenticated)
@get("/api/v1/users/me/bands")
async def get_my_groups(
    user: Optional[Identity],
) -> List[BandShortInfo]:
    """
    Получение списка групп авторизованного пользователя
    """
    return await get_user_groups(user.get("id"))
