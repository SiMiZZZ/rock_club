from pydantic import BaseModel, UUID4, ConfigDict

from models import User


class UserInfo(BaseModel):
    id: UUID4
    name: str
    surname: str
    email: str
    description: str

    model_config = ConfigDict(from_attributes=True)


async def get_user_info(user_id: str) -> UserInfo:
    user = await User.objects().where(User.id == user_id).first()
    return UserInfo.model_validate(user)
