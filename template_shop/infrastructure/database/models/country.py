from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from template_shop.infrastructure.database.models.base import TimedBaseModel

if TYPE_CHECKING:
    from .product import Product


class Country(TimedBaseModel):
    __tablename__ = "country"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    # categories: Mapped[list["Category"]] = relationship(secondary=countries_categories, back_populates="countries")
    products: Mapped[list["Product"]] = relationship(back_populates="country")

    def __repr__(self) -> str:
        return f"<Страна {self.name}>"

    def __str__(self) -> str:
        return self.__repr__()
