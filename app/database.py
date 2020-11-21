import logging

from peewee import Model
from peewee_async import Manager as DatabaseManager
from peewee_asyncext import PooledPostgresqlExtDatabase as Database

from .settings import settings

LOGGING_LEVEL = logging.DEBUG if settings.log_sql_queries else logging.INFO

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(LOGGING_LEVEL)
logger.propagate = False

db = Database(None)

db.set_allow_sync(settings.sync_db)  # migrations are synchronous
db_manager = DatabaseManager(db)
db.init(
    settings.postgres_db,
    user=settings.postgres_username,
    host=settings.postgres_host,
    port=settings.postgres_port,
    password=settings.postgres_password,
    min_connections=1,
    max_connections=settings.postgres_max_conn,
    connection_timeout=5,
)


async def connect_database() -> Database:
    return await db_manager.connect()


async def close_database() -> Database:
    return await db_manager.close()


class BaseModel(Model):
    objects: DatabaseManager = db_manager

    class Meta:
        database = db
