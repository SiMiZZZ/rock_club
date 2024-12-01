from piccolo.conf.apps import AppRegistry
from piccolo.engine import PostgresEngine

from config import settings

APP_REGISTRY = AppRegistry(apps=["config.piccolo_app"])
DB = PostgresEngine(
    config={
        "host": settings.DB_HOST,
        "port": settings.DB_PORT,
        "database": settings.DB_NAME,
        "user": settings.DB_USER,
        "password": settings.DB_PASSWORD,
        "statement_cache_size": 0,
    },
    log_queries=settings.DEBUG_SQL,
)
