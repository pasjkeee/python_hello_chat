from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config.settings import settings

db_url = URL.create(
    drivername=settings.driver,
    username=settings.username,
    password=settings.password,
    host=settings.host,
    port=settings.port,
    database=settings.database
)

engine = create_async_engine(
    db_url,
    echo=True,
    connect_args={"server_settings": {"search_path": settings.db_schema}}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,  # Не перезагружать объекты после коммита
)
