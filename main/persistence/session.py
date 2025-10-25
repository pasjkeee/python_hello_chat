from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from main.config.settings import settings

__db_url = URL.create(
    drivername=settings.db.driver,
    username=settings.db.username,
    password=settings.db.password.get_secret_value(),
    host=settings.db.host,
    port=settings.db.port,
    database=settings.db.database
)

__engine = create_async_engine(
    __db_url,
    echo=settings.db.debug,
    connect_args={"server_settings": {"search_path": settings.db.db_schema}}
)

AsyncSessionLocal = async_sessionmaker(
    bind=__engine,
    autoflush=False,
    expire_on_commit=False,  # Не перезагружать объекты после коммита
)
