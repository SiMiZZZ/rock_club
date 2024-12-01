from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from enum import Enum
from piccolo.columns.column_types import Varchar
from piccolo.columns.indexes import IndexMethod


ID = "2024-12-01T22:33:27:822931"
VERSION = "1.22.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="default", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="User",
        tablename="user",
        column_name="role",
        db_column_name="role",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "CLIENT",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum("UserRole", {"CLIENT": "CLIENT", "ADMIN": "ADMIN"}),
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    return manager
