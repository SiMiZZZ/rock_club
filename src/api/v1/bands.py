from typing import Optional, List

from blacksheep import post, get, FromFiles, patch
from blacksheep.exceptions import Forbidden
from guardpost import Identity
from pydantic import UUID4, BaseModel, HttpUrl

from api.exceptions import BandDoesNotExistException, NoFileData
from models import User
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
    get_band_or_none,
    BandUpdateInfo,
    update_band,
)
from services.s3.client import S3Client, FileType
from services.s3.types import File
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
@patch("/api/v1/bands/<band_id>")
async def update_band_info(
    band_id: UUID4, user_data: Optional[Identity], update_data: BandUpdateInfo
) -> BandInfo:
    band = await get_band_or_none(band_id)
    if band is None:
        raise BandDoesNotExistException
    if user_data.get("id") != str(band.leader):
        raise Forbidden()
    await update_band(band, update_data)
    return (await band_info(band.id)).ok()


@auth(authenticated)
@post("/api/v1/bands/<band_id>/members")
async def add_band_members(
    band_id: UUID4, members_ids: _BandMembers, user: Optional[Identity]
) -> EmptyObj:
    """
    Добавление участников в группу
    """
    band = await get_band_or_none(band_id)
    if band is None:
        raise BandDoesNotExistException
    if user.get("id") != str(band.leader):
        raise Forbidden()
    members = await User.objects().where(User.id.is_in(members_ids.members_ids))
    await add_members_to_band(band, members)
    return EmptyObj()


@auth(authenticated)
@post("/api/v1/bands/<band_id>/images/main")
async def add_band_main_image(
    files: FromFiles, band_id: UUID4, user_data: Optional[Identity]
) -> HttpUrl:
    band = await get_band_or_none(band_id)
    if band is None:
        raise BandDoesNotExistException
    if user_data.get("id") != str(band.leader):
        raise Forbidden()
    try:
        main_image = File.from_form_part(files.value[0])
    except IndexError:
        raise NoFileData()

    client = S3Client()
    file_link = client.upload_file(FileType.IMAGE, main_image)
    band.main_image = file_link
    await band.save()
    return file_link
