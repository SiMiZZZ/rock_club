from typing import List, Optional
import datetime

from pydantic import BaseModel, UUID4
from result import Result, Err, Ok

from models import Rehearsal
from services.types import DateRange, RehearsalInfo, TimeRange
from piccolo.columns.combination import And, Or

from services.users import get_user_or_none


class RehearsalCreate(BaseModel):
    band_id: Optional[UUID4]
    date: datetime.date
    time_from: datetime.time
    time_to: datetime.time
    is_individual: bool
    individual_user_id: Optional[UUID4]


async def get_rehearsal_by_id(rehearsal_id: UUID4) -> Rehearsal:
    rehearsal = await (
        Rehearsal.objects(Rehearsal.band.all_related()).where(
            Rehearsal.id == rehearsal_id
        )
    ).first()
    # FIXME: Некорректно работает префетч на юзера, нужно подробнее разобраться
    if rehearsal.is_individual:
        rehearsal.individual_user = await get_user_or_none(rehearsal.individual_user)
    return rehearsal


async def get_schedule_by_daterange(date_range: DateRange) -> List[RehearsalInfo]:
    rehearsals = await (
        Rehearsal.objects(
            Rehearsal.band.all_related(), Rehearsal.individual_user.all_related()
        )
        .where(Rehearsal.date >= date_range.start)
        .where(Rehearsal.date <= date_range.end)
        .order_by(Rehearsal.date)
    )
    for rehearsal in rehearsals:
        # FIXME: Некорректно работает префетч на юзера, нужно подробнее разобраться
        if rehearsal.is_individual:
            rehearsal.individual_user = await get_user_or_none(
                rehearsal.individual_user
            )
    return [await RehearsalInfo.from_rehearsal(rehearsal) for rehearsal in rehearsals]


async def create_rehearsal(rehearsal: RehearsalCreate) -> Result[Rehearsal, str]:
    time_range = TimeRange(rehearsal.time_from, rehearsal.time_to)
    async with Rehearsal._meta.db.transaction():
        await Rehearsal.select().where(Rehearsal.date == rehearsal.date).lock_rows()
        if await timerange_is_reserved(rehearsal.date, time_range):
            return Err("Данное время уже занято")
        if not rehearsal.is_individual:
            rehearsal = await Rehearsal.objects().create(
                is_individual=False,
                band=rehearsal.band_id,
                date=rehearsal.date,
                time_from=rehearsal.time_from,
                time_to=rehearsal.time_to,
                individual_user=None,
            )
        else:
            rehearsal = await Rehearsal.objects().create(
                is_individual=True,
                band=None,
                date=rehearsal.date,
                time_from=rehearsal.time_from,
                time_to=rehearsal.time_to,
                individual_user=rehearsal.individual_user_id,
            )
        return Ok(rehearsal)


async def timerange_is_reserved(date: datetime.date, time_range: TimeRange) -> bool:
    return await (
        Rehearsal.exists()
        .where(Rehearsal.date == date)
        .where(
            Or(
                Or(
                    And(
                        time_range.time_from >= Rehearsal.time_from,
                        time_range.time_from < Rehearsal.time_to,
                    ),
                    And(
                        time_range.time_to > Rehearsal.time_from,
                        time_range.time_to <= Rehearsal.time_to,
                    ),
                ),
                And(
                    time_range.time_from >= Rehearsal.time_from,
                    time_range.time_to <= Rehearsal.time_to,
                ),
            )
        )
    )
