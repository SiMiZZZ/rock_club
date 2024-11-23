from piccolo.table import Table
from piccolo import columns


class User(Table, tablename="user"):
    id = columns.UUID(primary_key=True)
    email = columns.Varchar()
    name = columns.Varchar()
    password = columns.Secret(length=255)
