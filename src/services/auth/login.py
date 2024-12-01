from asyncpg import UniqueViolationError
from result import Result, Ok, Err

from models import User
from services.auth.types import UserAuthInfo, RegisterUser, LoginUser
from services.auth.utils import hash_password, generate_user_token, verify_password


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
    new_user.access_token = generate_user_token(new_user)
    return Ok(new_user)


async def login_user(user: LoginUser) -> Result[UserAuthInfo, str]:
    orm_user = await User.objects().where(User.email == user.email).first()
    if not orm_user or not verify_password(user.password, orm_user.password):
        return Err("Неверные данные пользователя")
    new_user = UserAuthInfo.model_validate(orm_user)
    new_user.access_token = generate_user_token(new_user)
    return Ok(new_user)
