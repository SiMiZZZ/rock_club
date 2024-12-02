from typing import Optional

from pydantic import BaseModel, UUID4, ConfigDict, Field

from models import User


class UserInfo(BaseModel):
    id: UUID4
    name: str
    surname: str
    email: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdateInfo(BaseModel):
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


async def get_user_info(user_id: str) -> UserInfo:
    user = await User.objects().where(User.id == user_id).first()
    return UserInfo.model_validate(user)


async def update_user_info(user_id: str, info: UserUpdateInfo) -> None:
    await User.update(info.model_dump(exclude_none=True)).where(User.id == user_id)
