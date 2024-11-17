import json

from arq.connections import RedisSettings
from pydantic import BaseModel
from pydantic.v1 import validator


class DbConfig(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str
    echo: bool = False

    def full_url(self, with_driver: bool = True) -> str:
        login_data = f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        if with_driver:
            return f"postgresql+asyncpg://{login_data}"
        return f"postgresql://{login_data}"


class RedisConfig(BaseModel):
    host: str
    port: int
    database: int

    @property
    def url(self) -> str:
        return f"redis://@{self.host}:{self.port}/{self.database}"

    @property
    def pool_settings(self) -> RedisSettings:
        return RedisSettings(
            host=self.host,
            port=self.port,
            database=self.database,
        )


class TgBotConfig(BaseModel):
    token: str
    admin_ids: list[int]
    developer_id: int
    admin_channel_id: int
    channel_for_doc_drawing_orders: int
    use_redis: bool

    @validator("admin_ids", pre=True, always=True)
    def admin_ids_list(cls, v) -> list[int]:
        return json.loads(v)


class PaymentConfig(BaseModel):
    crypto_token: str


class Settings(BaseModel):
    tg_bot: TgBotConfig
    db: DbConfig
    redis: RedisConfig
    payment: PaymentConfig
