from typing import Optional

from blacksheep import post
from guardpost import Identity

from services.auth.types import authenticated
from blacksheep.server.authorization import auth

from services.bands import create_band, BandInfo, BandCreate


@auth(authenticated)
@post("/api/v1/bands")
async def create_new_band(user: Optional[Identity], band: BandCreate) -> BandInfo:
    return await create_band(user.get("id"), band)
