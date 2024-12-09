from typing import Optional, List, Self

from pydantic import BaseModel, ConfigDict, UUID4
from result import Result, Err, Ok

from models import User, Band, UserBands
from services.users import UserInfo


class BandCreate(BaseModel):
    name: str
    description: Optional[str]


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


async def get_band_or_none(band_id: str) -> Optional[Band]:
    return await Band.objects().where(Band.id == band_id).first()


async def create_band(leader_id: str, band_info: BandCreate) -> BandShortInfo:
    new_band = await Band.objects().create(
        name=band_info.name, description=band_info.description, leader=leader_id
    )

    new_band_with_leader = (
        await Band.objects()
        .prefetch(Band.leader.all_related())
        .get(Band.id == new_band.id)
    )

    leader = await User.objects().where(User.id == leader_id).first()

    await new_band.add_m2m(leader, m2m=Band.members)
    new_band_with_leader.leader = leader
    return await BandShortInfo.from_band(new_band_with_leader)


async def get_user_bands(user_id: str) -> List[BandShortInfo]:
    user_bands = await UserBands.objects(UserBands.band.leader).where(
        UserBands.user == user_id
    )
    return [await BandShortInfo.from_band(user_band.band) for user_band in user_bands]


async def band_info(band_id: UUID4) -> Result[BandInfo, str]:
    band = await Band.objects(Band.leader).where(Band.id == band_id).first()
    if band is None:
        return Err("Группы с таким id не существует")
    return Ok(await BandInfo.from_band(band))


async def add_members_to_band(band: Band, members: List[User]):
    await band.add_m2m(*members, m2m=Band.members)
