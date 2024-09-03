from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel
from .m2ms import products_orders

if TYPE_CHECKING:
    from .category import Category
    from .country import Country
    from .order import Order


class Product(TimedBaseModel):
    __tablename__ = "product"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[Decimal]
    link: Mapped[str]
    category: Mapped["Category"] = relationship(back_populates="products")
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    country: Mapped["Country"] = relationship(back_populates="products")
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    orders: Mapped[list["Order"]] = relationship(secondary=products_orders, back_populates="products")
    preview_image_path: Mapped[str | None]

    def __repr__(self) -> str:
        return f"<Товар №{self.id} {self.name}>"

    def __str__(self) -> str:
        return self.__repr__()
