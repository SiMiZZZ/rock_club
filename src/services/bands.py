from typing import Optional, List, Self

from pydantic import BaseModel, ConfigDict

from models import User, Band, UserBands
from services.users import UserInfo


class BandCreate(BaseModel):
    name: str
    description: Optional[str]


class BandInfo(BaseModel):
    name: str
    description: Optional[str]
    leader: UserInfo
    members: List[UserInfo]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_band(cls, band: Band) -> Self:
        return cls(
            name=band.name,
            description=band.description,
            leader=UserInfo.from_user(band.leader),
            members=[
                UserInfo.model_validate(member)
                for member in await band.get_m2m(Band.members)
            ],
        )


class BandShortInfo(BaseModel):
    name: str
    description: Optional[str]
    leader: UserInfo

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_band(cls, band: Band) -> Self:
        return cls(
            name=band.name,
            description=band.description,
            leader=UserInfo.from_user(band.leader),
        )


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


async def get_user_groups(user_id: str) -> List[BandShortInfo]:
    user_bands = await UserBands.objects(UserBands.band.leader).where(
        UserBands.user == user_id
    )
    return [await BandShortInfo.from_band(user_band.band) for user_band in user_bands]
