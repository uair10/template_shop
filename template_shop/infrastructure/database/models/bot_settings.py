from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class BotSettings(TimedBaseModel):
    __tablename__ = "bot_settings"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    bills_checker_enabled: Mapped[bool] = mapped_column(server_default="0")
    bills_checker_days: Mapped[int] = mapped_column(server_default="1")

    def __repr__(self) -> str:
        return f"<Настройки бота №{self.id}>"

    def __str__(self) -> str:
        return self.__repr__()
