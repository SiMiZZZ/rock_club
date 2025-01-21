import datetime

from blacksheep import get, FromQuery, post

from api.exceptions import (
    NotValidDateIntervalException,
    ReservedTimeRangeException,
    BandDoesNotExistException,
)
from services.bands import get_band_or_none

from services.schedule import (
    get_schedule_by_daterange,
    RehearsalCreate,
    create_rehearsal,
    get_rehearsal_by_id,
)
from services.types import DateRange, RehearsalInfo


@get("/api/v1/schedule")
async def get_schedule(
    date_from: FromQuery[datetime.date], date_to: FromQuery[datetime.date]
):
    date_range = DateRange.try_from(date_from.value, date_to.value).unwrap_or_raise(
        NotValidDateIntervalException
    )

    schedule = await get_schedule_by_daterange(date_range)
    return schedule


@post("/api/v1/schedule/rehearsal")
async def create_new_rehearsal(rehearsal: RehearsalCreate) -> RehearsalInfo:
    if not rehearsal.is_individual:
        band = await get_band_or_none(rehearsal.band_id)
        if band is None:
            raise BandDoesNotExistException
    new_rehearsal = (await create_rehearsal(rehearsal)).unwrap_or_raise(
        ReservedTimeRangeException
    )
    new_rehearsal = await get_rehearsal_by_id(new_rehearsal.id)
    return await RehearsalInfo.from_rehearsal(new_rehearsal)
