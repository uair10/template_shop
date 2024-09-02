from template_shop.admin_panel.app.views import MyBaseModelView


class SettingsModelView(MyBaseModelView):
    column_labels = {
        "certificate": "Лимит в складчине по сертификатам",
        "declaration": "Лимит в складчине по декларациям",
        "declaration_gost": "Лимит в складчине по декларациям ГОСТ",
        "letter": "Лимит в складчине по отказным",
        "sgr": "Лимит в складчине по СГР",
        "sgr_declaration": "Лимит в складчине по СГР + Декларации",
        "bills_checker_enabled": "Проверка оплат включена",
        "bills_checker_days": "За сколько дней проверять оплату",
        "referral_notify_enabled": "Отправка уведомлений о рефералах включена",
    }

    column_exclude_list = "description"
