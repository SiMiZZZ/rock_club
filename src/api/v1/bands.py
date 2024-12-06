from typing import Optional, List

from blacksheep import post, get
from guardpost import Identity
from pydantic import UUID4

from api.exceptions import BandDoesNotExistException
from services.auth.types import authenticated
from blacksheep.server.authorization import auth

from services.bands import (
    create_band,
    BandCreate,
    get_user_bands,
    BandShortInfo,
    band_info,
    BandInfo,
)


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
    return await get_user_bands(user.get("id"))


@get("/api/v1/bands/<band_id>")
async def get_band_info(band_id: UUID4) -> BandInfo:
    band = await band_info(band_id)
    return band.unwrap_or_raise(BandDoesNotExistException)
