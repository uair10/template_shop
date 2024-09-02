"""Initial

Revision ID: 4eb09b0e943e
Revises:
Create Date: 2024-09-02 17:23:31.663626

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4eb09b0e943e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "admin_user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("can_create_admins", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("can_export", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("can_delete", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("can_edit", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("can_add", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("can_view_files", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_admin_user")),
        sa.UniqueConstraint("email", name=op.f("uq_admin_user_email")),
    )
    op.create_table(
        "bot_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bills_checker_enabled", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("bills_checker_days", sa.Integer(), server_default="1", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_bot_settings")),
    )
    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_category")),
    )
    op.create_table(
        "country",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_country")),
    )
    op.create_table(
        "promocode",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "type",
            sa.Enum("bonus", "balance", "discount", name="promocodetype"),
            server_default="balance",
            nullable=False,
        ),
        sa.Column("amount", sa.Numeric(), nullable=False),
        sa.Column(
            "status", sa.Enum("active", "archive", name="promocodestatus"), server_default="active", nullable=False
        ),
        sa.Column("limit", sa.Integer(), server_default="0", nullable=False),
        sa.Column("reusable", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("uses_number", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_promocode")),
    )
    op.create_table(
        "stats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("products_purchased", sa.Integer(), server_default="0", nullable=False),
        sa.Column("orders_created", sa.Integer(), server_default="0", nullable=False),
        sa.Column("users_registered", sa.Integer(), server_default="0", nullable=False),
        sa.Column("payments_paid", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_stats")),
        sa.UniqueConstraint("date", name=op.f("uq_stats_date")),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("balance", sa.Numeric(), server_default="0", nullable=False),
        sa.Column("lang_code", sa.Enum("ru", "en", name="langcode"), server_default="ru", nullable=False),
        sa.Column("was_registered", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("telegram_id", name=op.f("uq_user_telegram_id")),
    )
    op.create_table(
        "bill",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("payment_method", sa.Enum("crypto", name="paymentmethod"), nullable=False),
        sa.Column("summ", sa.Numeric(), nullable=False),
        sa.Column("invoice_id", sa.String(length=50), nullable=False),
        sa.Column(
            "status",
            sa.Enum("paid", "waiting_payment", "payment_failed", name="billstatus"),
            server_default="waiting_payment",
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("promocode_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["promocode_id"], ["promocode.id"], name=op.f("fk_bill_promocode_id_promocode")),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_bill_user_id_user")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_bill")),
    )
    op.create_table(
        "countries_categories",
        sa.Column("country_id", sa.Integer(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"], ["category.id"], name=op.f("fk_countries_categories_category_id_category")
        ),
        sa.ForeignKeyConstraint(
            ["country_id"], ["country.id"], name=op.f("fk_countries_categories_country_id_country")
        ),
    )
    op.create_table(
        "order",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("summ", sa.Float(), nullable=False),
        sa.Column("promocode_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["promocode_id"], ["promocode.id"], name=op.f("fk_order_promocode_id_promocode")),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_order_user_id_user")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_order")),
    )
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column("link", sa.String(), nullable=False),
        sa.Column("link_password", sa.String(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("preview_image_path", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["category.id"], name=op.f("fk_product_category_id_category")),
        sa.ForeignKeyConstraint(["country_id"], ["country.id"], name=op.f("fk_product_country_id_country")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product")),
    )
    op.create_table(
        "promocodes_users",
        sa.Column("promocode_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["promocode_id"], ["promocode.id"], name=op.f("fk_promocodes_users_promocode_id_promocode")
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_promocodes_users_user_id_user")),
    )
    op.create_table(
        "orders_users",
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["order_id"], ["order.id"], name=op.f("fk_orders_users_order_id_order")),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_orders_users_user_id_user")),
    )
    op.create_table(
        "products_orders",
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["order_id"], ["order.id"], name=op.f("fk_products_orders_order_id_order")),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"], name=op.f("fk_products_orders_product_id_product")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("products_orders")
    op.drop_table("orders_users")
    op.drop_table("promocodes_users")
    op.drop_table("product")
    op.drop_table("order")
    op.drop_table("countries_categories")
    op.drop_table("bill")
    op.drop_table("user")
    op.drop_table("stats")
    op.drop_table("promocode")
    op.drop_table("country")
    op.drop_table("category")
    op.drop_table("bot_settings")
    op.drop_table("admin_user")
    # ### end Alembic commands ###