import orjson
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from template_shop.core.config import DbConfig


def build_sa_engine(db_config: DbConfig) -> AsyncEngine:
    return create_async_engine(
        db_config.full_url(),
        echo_pool=db_config.echo,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
        pool_recycle=1800,
        pool_pre_ping=True,
    )


def build_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine, future=True, autoflush=False, expire_on_commit=False)
