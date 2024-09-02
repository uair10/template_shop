from sqlalchemy import Column, ForeignKey, Integer, Table

from template_shop.infrastructure.database.models.base import TimedBaseModel

orders_users = Table(
    "orders_users",
    TimedBaseModel.metadata,
    Column("order_id", Integer, ForeignKey("order.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
)

promocodes_users = Table(
    "promocodes_users",
    TimedBaseModel.metadata,
    Column("promocode_id", Integer, ForeignKey("promocode.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
)

countries_categories = Table(
    "countries_categories",
    TimedBaseModel.metadata,
    Column("country_id", Integer, ForeignKey("country.id")),
    Column("category_id", Integer, ForeignKey("category.id")),
)

products_orders = Table(
    "products_orders",
    TimedBaseModel.metadata,
    Column("product_id", Integer, ForeignKey("product.id")),
    Column("order_id", Integer, ForeignKey("order.id")),
)
