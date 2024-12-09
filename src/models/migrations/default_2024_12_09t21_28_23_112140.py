from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Varchar


ID = "2024-12-09T21:28:23:112140"
VERSION = "1.22.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="default", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="User",
        tablename="user",
        column_name="main_image",
        db_column_name="main_image",
        params={"null": True},
        old_params={"null": False},
        column_class=Varchar,
        old_column_class=Varchar,
        schema=None,
    )

    return manager
