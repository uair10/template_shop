from template_shop.admin_panel.app.views import MyBaseModelView


class OrderModelView(MyBaseModelView):
    column_list = (
        "id",
        "status",
        "summ",
        "promocode",
        "user",
    )

    column_filters = ("summ",)

    column_labels = {
        "status": "Статус",
        "products": "Товары",
        "type": "Тип заказа",
        "summ": "Сумма",
        "promocode": "Промокод",
        "user": "Покупатель",
    }
