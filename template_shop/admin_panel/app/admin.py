from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login import current_user

from template_shop.admin_panel.app import db
from template_shop.admin_panel.app.views import (
    AdminUserBaseModelview,
    BillsModelView,
    CountryModelView,
    MyAdminIndexView,
    OrderModelView,
    ProductModelView,
    PromocodesModelView,
    SettingsModelView,
    StatsModelView,
    UserModelView,
)
from template_shop.admin_panel.app.views.category import CategoryModelView
from template_shop.infrastructure.database.models import (
    AdminUser,
    Bill,
    BotSettings,
    Category,
    Country,
    Order,
    Product,
    Promocode,
    Statistics,
    User,
)


class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated


def init_admin_panel(app):
    admin = Admin(
        app,
        name="Admin Dashboard",
        base_template="myadmin3/my_master.html",
        template_mode="bootstrap4",
        index_view=MyAdminIndexView(url="/"),
    )

    admin.add_view(
        UserModelView(
            User,
            db.session,
            name="Пользователи",
            menu_icon_type="fas",
            menu_icon_value="fa-user",
            endpoint="users",
        ),
    )
    admin.add_view(
        CountryModelView(
            Country,
            db.session,
            name="Страны",
            menu_icon_type="fas",
            menu_icon_value="fa-list",
            endpoint="countries",
        ),
    )
    admin.add_view(
        CategoryModelView(
            Category,
            db.session,
            name="Категории",
            menu_icon_type="fas",
            menu_icon_value="fa-list",
            endpoint="categories",
        ),
    )
    admin.add_view(
        ProductModelView(
            Product,
            db.session,
            name="Товары",
            menu_icon_type="fas",
            menu_icon_value="fa-cubes",
            endpoint="products",
        ),
    )
    admin.add_view(
        OrderModelView(
            Order,
            db.session,
            name="Заказы",
            menu_icon_type="fas",
            menu_icon_value="fa-shopping-cart",
            endpoint="orders",
        ),
    )
    admin.add_view(
        BillsModelView(
            Bill,
            db.session,
            name="Счета пользователям",
            menu_icon_type="fas",
            menu_icon_value="fa-money",
            endpoint="bills",
        ),
    )
    admin.add_view(
        PromocodesModelView(
            Promocode,
            db.session,
            name="Промокоды",
            menu_icon_type="fas",
            menu_icon_value="fa-dollar",
            endpoint="promocodes",
        ),
    )
    admin.add_view(
        SettingsModelView(
            BotSettings,
            db.session,
            name="Настройки бота",
            menu_icon_type="fas",
            menu_icon_value="fa-gears",
            endpoint="bot_settings",
        ),
    )
    admin.add_view(
        StatsModelView(
            Statistics,
            db.session,
            name="Статистика",
            menu_icon_type="fas",
            menu_icon_value="fa-bar-chart",
            endpoint="statistic",
        ),
    )
    admin.add_view(
        AdminUserBaseModelview(
            AdminUser,
            db.session,
            name="Администраторы",
            menu_icon_type="fas",
            menu_icon_value="fa-users",
            endpoint="admin-user",
        ),
    )
