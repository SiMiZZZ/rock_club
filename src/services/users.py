from typing import Optional, List

from piccolo.query.functions.string import Concat
from pydantic import BaseModel, Field
from models import User
from services.types import UserInfo


class UserUpdateInfo(BaseModel):
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


async def get_user_or_none(user_id: str) -> Optional[User]:
    return await User.objects().where(User.id == user_id).first()


async def get_user_info_by_id(user_id: str) -> UserInfo:
    user = await User.objects().where(User.id == user_id).first()
    return UserInfo.model_validate(user)


async def get_user_info(user: User) -> UserInfo:
    return UserInfo.model_validate(user)


async def update_user_info(user_id: str, info: UserUpdateInfo) -> None:
    await User.update(info.model_dump(exclude_none=True)).where(User.id == user_id)


async def find_users_by_substring(substring: str) -> List[UserInfo]:
    full_name = Concat(User.surname, " ", User.name)
    users = await User.objects().where(full_name.ilike(f"%{substring}%"))
    return [UserInfo.from_user(user) for user in users]
