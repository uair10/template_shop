import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from template_shop.infrastructure.database.models.base import TimedBaseModel


class Statistics(TimedBaseModel):
    __tablename__ = "stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(unique=True, server_default=func.now())
    products_purchased: Mapped[int] = mapped_column(server_default="0")
    orders_created: Mapped[int] = mapped_column(server_default="0")
    users_registered: Mapped[int] = mapped_column(server_default="0")
    payments_paid: Mapped[int] = mapped_column(server_default="0")

    def __repr__(self) -> str:
        return f"<Статистика №{self.id} за день {self.date}>"
