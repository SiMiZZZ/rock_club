from piccolo.columns import ForeignKey, LazyTableReference
from piccolo.columns.m2m import M2M
from piccolo.table import Table
from piccolo import columns
from .users import User
import uuid


class Band(Table, tablename="band"):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    leader = ForeignKey(User, related_name="leader_bands")
    name = columns.Varchar()
    description = columns.Text(null=True)
    members = M2M(LazyTableReference("user_bands", module_path=__name__))


class UserBands(Table, tablename="user_band"):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user = ForeignKey(User, target_column="id")
    band = ForeignKey(Band, target_column="id")
