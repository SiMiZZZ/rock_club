from piccolo.table import Table
from piccolo import columns
import uuid

from services.auth.types import UserRole


class User(Table, tablename="user"):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    email = columns.Varchar(unique=True)
    name = columns.Varchar()
    surname = columns.Varchar()
    role = columns.Varchar(choices=UserRole, default=UserRole.CLIENT)
    description = columns.Text(null=True)
    password = columns.Secret(length=255)
