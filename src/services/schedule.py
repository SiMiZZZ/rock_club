from typing import List


from models import Rehearsal
from services.types import DateRange, RehearsalInfo


async def get_schedule_by_daterange(date_range: DateRange) -> List[RehearsalInfo]:
    rehearsals = await (
        Rehearsal.objects(
            Rehearsal.band.all_related(), Rehearsal.individual_user.all_related()
        )
        .where(Rehearsal.date >= date_range.start)
        .where(Rehearsal.date <= date_range.end)
        .order_by(Rehearsal.date)
    )
    return [await RehearsalInfo.from_rehearsal(rehearsal) for rehearsal in rehearsals]
