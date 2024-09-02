from template_shop.admin_panel.app.views import MyBaseModelView


class StatsModelView(MyBaseModelView):
    column_list = (
        "date",
        "products_purchased",
        "orders_created",
        "users_registered",
        "payments_paid",
    )

    column_labels = {
        "date": "День",
        "products_purchased": "Куплено товаров",
        "orders_created": "Создано заказов",
        "users_registered": "Зарегистрировалось пользователей",
        "payments_paid": "Оплачено счетов",
    }

    column_filters = column_list

    column_default_sort = ("id", True)
