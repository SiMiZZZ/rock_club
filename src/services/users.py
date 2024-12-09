from typing import Optional, Self, List

from piccolo.query.functions.string import Concat
from pydantic import BaseModel, UUID4, ConfigDict, Field
from models import User


class UserInfo(BaseModel):
    id: UUID4
    name: str
    surname: str
    email: str
    description: str
    main_image: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_user(cls, user: User) -> Self:
        return cls(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            description=user.description,
            main_image=user.main_image,
        )


class UserUpdateInfo(BaseModel):
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


async def get_user_or_none(user_id: str) -> Optional[User]:
    return await User.objects().where(User.id == user_id).first()


async def get_user_info(user_id: str) -> UserInfo:
    user = await User.objects().where(User.id == user_id).first()
    return UserInfo.model_validate(user)


async def update_user_info(user_id: str, info: UserUpdateInfo) -> None:
    await User.update(info.model_dump(exclude_none=True)).where(User.id == user_id)


async def find_users_by_substring(substring: str) -> List[UserInfo]:
    full_name = Concat(User.surname, " ", User.name)
    users = await User.objects().where(full_name.ilike(f"%{substring}%"))
    return [UserInfo.from_user(user) for user in users]
