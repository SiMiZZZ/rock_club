from asyncpg import UniqueViolationError
from result import Result, Ok, Err

from models import User
from services.auth.types import UserAuthInfo, RegisterUser, JwtPayload
from services.auth.utils import hash_password, encode_jwt


async def register_user(user: RegisterUser) -> Result[UserAuthInfo, str]:
    try:
        orm_user = await User.objects().create(
            name=user.name,
            surname=user.surname,
            email=user.email,
            password=hash_password(user.password).decode(),
        )

    except UniqueViolationError:
        return Err("Пользователь с таким email уже зарегистрирован")
    new_user = UserAuthInfo.model_validate(orm_user)
    new_user.access_token = encode_jwt(
        JwtPayload(id=str(new_user.id), email=user.email)
    )
    return Ok(new_user)
