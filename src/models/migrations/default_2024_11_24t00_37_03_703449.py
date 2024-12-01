from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Varchar


ID = "2024-11-24T00:37:03:703449"
VERSION = "1.22.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="default", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="User",
        tablename="user",
        column_name="email",
        db_column_name="email",
        params={"unique": True},
        old_params={"unique": False},
        column_class=Varchar,
        old_column_class=Varchar,
        schema=None,
    )

    return manager
