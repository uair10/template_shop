import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from template_shop.core.models.enums.user import LangCode
from template_shop.infrastructure.database.models.base import TimedBaseModel
from template_shop.infrastructure.database.models.m2ms import promocodes_users

if TYPE_CHECKING:
    from .bill import Bill
    from .order import Order
    from .promocode import Promocode


class User(TimedBaseModel):
    __tablename__ = "user"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(50))
    balance: Mapped[Decimal] = mapped_column(server_default="0")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    promocodes: Mapped[list["Promocode"]] = relationship(secondary=promocodes_users, back_populates="users")
    bills: Mapped[list["Bill"]] = relationship(back_populates="user")
    lang_code: Mapped[LangCode] = mapped_column(server_default="ru")
    was_registered: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    def __repr__(self) -> str:
        return f"<Пользователь №{self.id} {self.telegram_id}>"

    def __str__(self) -> str:
        return self.__repr__()
