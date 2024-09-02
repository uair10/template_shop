from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel
from .m2ms import products_orders

if TYPE_CHECKING:
    from .product import Product
    from .promocode import Promocode
    from .user import User


class Order(TimedBaseModel):
    __tablename__ = "order"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    products: Mapped[list["Product"]] = relationship(secondary=products_orders, back_populates="orders")
    summ: Mapped[float] = mapped_column(nullable=False)
    promocode: Mapped["Promocode"] = relationship(back_populates="orders")
    promocode_id: Mapped[int | None] = mapped_column(ForeignKey("promocode.id"))
    user: Mapped["User"] = relationship(back_populates="orders")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"<Заказ №{self.id} {self.created_at}>"

    def __str__(self) -> str:
        return self.__repr__()
