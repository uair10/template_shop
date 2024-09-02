from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from template_shop.core.models.enums.bill import BillStatus, PaymentMethod

from .base import TimedBaseModel

if TYPE_CHECKING:
    from .promocode import Promocode
    from .user import User


class Bill(TimedBaseModel):
    __tablename__ = "bill"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_method: Mapped[PaymentMethod]
    summ: Mapped[Decimal]
    invoice_id: Mapped[str] = mapped_column(String(50))
    status: Mapped[BillStatus] = mapped_column(server_default="waiting_payment")
    user: Mapped["User"] = relationship(back_populates="bills")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    promocode: Mapped["Promocode"] = relationship(back_populates="bills")
    promocode_id: Mapped[int | None] = mapped_column(ForeignKey("promocode.id"))

    def __repr__(self) -> str:
        return f"<Счет №{self.id} на сумму {self.summ}$>"

    def __str__(self) -> str:
        return self.__repr__()
