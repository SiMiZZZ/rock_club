from enum import StrEnum
from typing import final

from pydantic import BaseModel, EmailStr, ConfigDict, UUID4
from dataclasses import dataclass


authenticated = "authenticated"


class UserRole(StrEnum):
    CLIENT = "CLIENT"
    ADMIN = "ADMIN"


class UserAuthInfo(BaseModel):
    id: UUID4
    email: EmailStr
    name: str
    surname: str
    main_image: str
    role: UserRole
    access_token: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RegisterUser(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


@final
@dataclass(frozen=True)
class JwtPayload:
    id: str
    email: EmailStr
    role: str
