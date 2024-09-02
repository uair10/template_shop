from template_shop.admin_panel.app.views import MyBaseModelView


class BillsModelView(MyBaseModelView):
    column_list = (
        "id",
        "status",
        "payment_method",
        "summ",
        "user",
        "invoice_id",
        "created_at",
    )

    column_labels = {
        "summ": "Сумма",
        "invoice_id": "Номер платежа в кассе",
        "payment_method": "Метод оплаты",
        "status": "Статус",
        "user": "Пользователь",
        "promocode": "Промокод",
    }

    column_filters = (
        "invoice_id",
        "status",
        "summ",
        "promocode",
        "created_at",
    )

    column_default_sort = ("id", True)
