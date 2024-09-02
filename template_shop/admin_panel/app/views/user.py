from template_shop.admin_panel.app.views import MyBaseModelView


class UserModelView(MyBaseModelView):
    column_list = (
        "id",
        "telegram_id",
        "username",
        "balance",
        "lang_code",
        "was_registered",
    )

    column_searchable_list = (
        "telegram_id",
        "username",
    )

    column_filters = (
        "telegram_id",
        "username",
        "balance",
        "was_registered",
    )

    column_labels = {
        "status": "Статус",
        "telegram_id": "ID в телеграме",
        "username": "Юзернейм в телеграме",
        "balance": "Баланс",
        "lang_code": "Язык",
        "was_created": "Дата создания",
        "orders": "Заказы",
        "promocodes": "Введенные промокоды",
        "bills": "Счета",
        "was_registered": "Дата регистрации",
    }

    column_default_sort = ("id", True)
