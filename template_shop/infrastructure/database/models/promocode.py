import enum
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from template_shop.core.models.enums.promocode import PromocodeType
from template_shop.infrastructure.database.models.base import TimedBaseModel
from template_shop.infrastructure.database.models.m2ms import promocodes_users

if TYPE_CHECKING:
    from .bill import Bill
    from .order import Order
    from .user import User


class PromocodeStatus(enum.Enum):
    active = "active"
    archive = "archive"


class Promocode(TimedBaseModel):
    __tablename__ = "promocode"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[PromocodeType] = mapped_column(server_default="balance")
    amount: Mapped[Decimal]
    status: Mapped[PromocodeStatus] = mapped_column(
        server_default="active",
    )
    users: Mapped[list["User"]] = relationship(secondary=promocodes_users, back_populates="promocodes")
    orders: Mapped[list["Order"]] = relationship(back_populates="promocode")
    bills: Mapped[list["Bill"]] = relationship(back_populates="promocode")
    limit: Mapped[int] = mapped_column(server_default="0")
    reusable: Mapped[bool] = mapped_column(server_default="0")
    uses_number: Mapped[int] = mapped_column(server_default="0")

    def __repr__(self) -> str:
        return f"<Промокод №{self.id} {self.name}>"

    def __str__(self) -> str:
        return self.__repr__()
