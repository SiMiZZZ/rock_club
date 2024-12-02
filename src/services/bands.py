from typing import Optional

from pydantic import BaseModel, ConfigDict

from models import User, Band
from services.users import UserInfo


class BandCreate(BaseModel):
    name: str
    description: Optional[str]


class BandInfo(BaseModel):
    name: str
    description: Optional[str]
    leader: UserInfo

    model_config = ConfigDict(from_attributes=True)


async def create_band(leader_id: str, band_info: BandCreate) -> BandInfo:
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
    band_info = BandInfo.model_validate(new_band_with_leader)
    return band_info
