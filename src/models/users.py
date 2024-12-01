from piccolo.table import Table
from piccolo import columns
import uuid


class User(Table, tablename="user"):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    email = columns.Varchar(unique=True)
    name = columns.Varchar()
    surname = columns.Varchar()
    password = columns.Secret(length=255)
