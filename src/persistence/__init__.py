from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config.settings import settings

db_url = URL.create(
    drivername=settings.db.driver,
    username=settings.db.username,
    password=settings.db.password.get_secret_value(),
    host=settings.db.host,
    port=settings.db.port,
    database=settings.db.database
)

engine = create_async_engine(
    db_url,
    echo=settings.db.debug,
    connect_args={"server_settings": {"search_path": settings.db.db_schema}}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,  # Не перезагружать объекты после коммита
)
