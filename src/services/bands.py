from typing import Optional, List

from pydantic import BaseModel, UUID4
from result import Result, Err, Ok

from models import User, Band, UserBands
from services.types import BandInfo, BandShortInfo


class BandCreate(BaseModel):
    name: str
    description: Optional[str]


class BandUpdateInfo(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


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


async def update_band(band: Band, info: BandUpdateInfo) -> None:
    await Band.update(info.model_dump(exclude_none=True)).where(Band.id == band.id)


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
