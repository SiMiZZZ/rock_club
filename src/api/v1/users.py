from typing import Optional, List

from blacksheep import get, patch, post
from blacksheep import FromFiles
from guardpost import Identity
from pydantic import HttpUrl, UUID4

from api.exceptions import NoFileData, InvalidUserDataException
from services.auth.types import authenticated
from blacksheep.server.authorization import auth

from services.s3.client import S3Client, FileType
from services.s3.types import File
from services.users import (
    get_user_info_by_id,
    UserUpdateInfo,
    update_user_info,
    find_users_by_substring,
    get_user_or_none,
    get_user_info,
)
from services.types import UserInfo


@auth(authenticated)
@get("/api/v1/users/me")
async def auth_user_info(user: Optional[Identity]) -> UserInfo:
    """
    Получение информации об авторизованном пользователе
    """
    return await get_user_info_by_id(user.get("id"))


@get("/api/v1/users/<user_id>")
async def user_info(user_id: UUID4) -> UserInfo:
    """
    Получение информации об авторизованном пользователе
    """
    user = await get_user_or_none(user_id)
    if user is None:
        raise InvalidUserDataException()
    return await get_user_info(user)


@auth(authenticated)
@patch("/api/v1/users/me")
async def update_self_user(
    user: Optional[Identity], update_info: UserUpdateInfo
) -> UserInfo:
    """
    Обновление информации об авторизованном пользователе
    """
    await update_user_info(user.get("id"), update_info)
    return await get_user_info_by_id(user.get("id"))


@get("/api/v1/users/find/{substring}")
async def find_users(substring: str) -> List[UserInfo]:
    return await find_users_by_substring(substring)


@auth(authenticated)
@post("/api/v1/users/me/images/main")
async def add_main_image(files: FromFiles, user_data: Optional[Identity]) -> HttpUrl:
    try:
        main_image = File.from_form_part(files.value[0])
    except IndexError:
        raise NoFileData()

    client = S3Client()
    file_link = client.upload_file(FileType.IMAGE, main_image)
    user = await get_user_or_none(user_data.get("id"))
    if user is not None:
        user.main_image = file_link
        await user.save()
    return file_link
