from piccolo.columns import ForeignKey
from piccolo.table import Table
from piccolo import columns
from .users import User
import uuid


class Band(Table, tablename="band"):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    leader = ForeignKey(User, related_name="leader_bands")
    name = columns.Varchar()
    description = columns.Text(null=True)


class UserBands(Table, tablename="user_band"):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user = ForeignKey(User, target_column="id")
    band = ForeignKey(Band, target_column="id")
