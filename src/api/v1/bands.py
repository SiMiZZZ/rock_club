from typing import Optional, List

from blacksheep import post, get
from blacksheep.exceptions import Forbidden
from guardpost import Identity
from pydantic import UUID4, BaseModel

from api.exceptions import BandDoesNotExistException
from models import Band, User
from services.auth.types import authenticated
from blacksheep.server.authorization import auth

from services.bands import (
    create_band,
    BandCreate,
    get_user_bands,
    BandShortInfo,
    band_info,
    BandInfo,
    add_members_to_band,
)
from services.types import EmptyObj


class _BandMembers(BaseModel):
    members_ids: List[UUID4]


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
    """
    Получение информации о группе
    """
    band = await band_info(band_id)
    return band.unwrap_or_raise(BandDoesNotExistException)


@auth(authenticated)
@post("/api/v1/bands/<band_id>/members")
async def add_band_members(
    band_id: UUID4, members_ids: _BandMembers, user: Optional[Identity]
) -> EmptyObj:
    """
    Добавление участников в группу
    """
    band = await Band.objects().where(Band.id == band_id).first()
    if not band:
        raise BandDoesNotExistException
    if user.get("id") != str(band.leader):
        raise Forbidden()
    members = await User.objects().where(User.id.is_in(members_ids.members_ids))
    await add_members_to_band(band, members)
    return EmptyObj()
