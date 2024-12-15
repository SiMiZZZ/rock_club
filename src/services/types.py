import dataclasses
import datetime
from typing import Optional, List, Self

from pydantic import BaseModel, UUID4, ConfigDict
from result import Result, Err, Ok

from models import Band, User, Rehearsal


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


@dataclasses.dataclass(frozen=True, slots=True)
class DateRange:
    start: datetime.date
    end: datetime.date

    @classmethod
    def try_from(cls, start: datetime.date, end: datetime.date) -> Result[Self, None]:
        if start > end:
            return Err(None)
        return Ok(DateRange(start, end))


class RehearsalInfo(BaseModel):
    id: UUID4
    band: Optional[BandShortInfo]
    date: datetime.date
    time_from: datetime.time
    time_to: datetime.time
    is_individual: bool
    individual_user: Optional[UserInfo]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_rehearsal(cls, rehearsal: Rehearsal) -> Self:
        return cls(
            id=rehearsal.id,
            band=await BandShortInfo.from_band(rehearsal.band)
            if not rehearsal.is_individual
            else None,
            date=rehearsal.date,
            time_from=rehearsal.time_from,
            time_to=rehearsal.time_to,
            is_individual=rehearsal.is_individual,
            individual_user=UserInfo.from_user(await rehearsal.individual_user)
            if rehearsal.is_individual
            else None,
        )
