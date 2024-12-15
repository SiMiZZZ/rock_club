from typing import Optional, List, Self

from pydantic import BaseModel, UUID4, ConfigDict

from models import Band, User


class EmptyObj(BaseModel):
    """Объект-пустышка"""


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


class BandInfo(BaseModel):
    id: UUID4
    name: str
    description: Optional[str]
    leader: UserInfo
    main_image: Optional[str]
    members: List[UserInfo]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_band(cls, band: Band) -> Self:
        return cls(
            id=band.id,
            name=band.name,
            description=band.description,
            leader=UserInfo.from_user(band.leader),
            main_image=band.main_image,
            members=[
                UserInfo.model_validate(member)
                for member in await band.get_m2m(Band.members)
            ],
        )


class BandShortInfo(BaseModel):
    id: UUID4
    name: str
    description: Optional[str]
    main_image: Optional[str]
    leader: UserInfo

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_band(cls, band: Band) -> Self:
        return cls(
            id=band.id,
            name=band.name,
            description=band.description,
            leader=UserInfo.from_user(band.leader),
            main_image=band.main_image,
        )
