from asyncpg import UniqueViolationError
from blacksheep import post
from services.users import RegisterUser
from models.users import User
from services.auth.types import UserAuthInfo
from blacksheep.exceptions import HTTPException


@post("/api/v1/auth/register")
async def register_user(user: RegisterUser) -> UserAuthInfo:
    try:
        orm_user = await User.objects().create(
            name=user.name,
            surname=user.surname,
            email=user.email,
            password=user.password,
        )
        new_user = UserAuthInfo.model_validate(orm_user)
    except UniqueViolationError:
        raise HTTPException(
            409, message="Пользователь с таким email уже зарегистрирован"
        )
    return new_user
