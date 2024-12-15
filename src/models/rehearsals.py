from piccolo.columns import ForeignKey
from piccolo.table import Table
from piccolo import columns

from . import Band
from .users import User
import uuid


class Rehearsal(Table, tablename="rehearsal"):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    band = ForeignKey(Band, related_name="band_rehearsals", required=False, null=True)
    date = columns.Date(required=True)
    time_from = columns.Time(required=True)
    time_to = columns.Time(required=True)
    is_individual = columns.Boolean(default=False)
    individual_user = columns.ForeignKey(
        User, related_name="individual_rehearsals", null=True
    )
