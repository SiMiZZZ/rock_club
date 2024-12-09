from typing import Optional, List

from blacksheep import get, patch, post
from blacksheep import FromFiles
from guardpost import Identity

from api.exceptions import NoFileData
from services.auth.types import authenticated
from blacksheep.server.authorization import auth

from services.s3.client import S3Client, FileType
from services.s3.types import File
from services.users import (
    get_user_info,
    UserInfo,
    UserUpdateInfo,
    update_user_info,
    find_users_by_substring,
    get_user_or_none,
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


@auth(authenticated)
@post("/api/v1/users/me/images/main")
async def add_main_image(files: FromFiles, user_data: Optional[Identity]) -> str:
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
