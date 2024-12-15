import datetime

from blacksheep import get, FromQuery

from api.exceptions import NotValidDateIntervalException

from services.schedule import get_schedule_by_daterange
from services.types import DateRange


@get("/api/v1/schedule")
async def get_schedule(
    date_from: FromQuery[datetime.date], date_to: FromQuery[datetime.date]
):
    date_range = DateRange.try_from(date_from.value, date_to.value).unwrap_or_raise(
        NotValidDateIntervalException
    )

    schedule = await get_schedule_by_daterange(date_range)
    return schedule
