from typing import Optional, Self

from pydantic import BaseModel, UUID4, ConfigDict, Field

from models import User


class UserInfo(BaseModel):
    id: UUID4
    name: str
    surname: str
    email: str
    description: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_user(cls, user: User) -> Self:
        return cls(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            description=user.description,
        )


class UserUpdateInfo(BaseModel):
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


async def get_user_info(user_id: str) -> UserInfo:
    user = await User.objects().where(User.id == user_id).first()
    return UserInfo.model_validate(user)


async def update_user_info(user_id: str, info: UserUpdateInfo) -> None:
    await User.update(info.model_dump(exclude_none=True)).where(User.id == user_id)
