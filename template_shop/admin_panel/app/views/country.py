from template_shop.admin_panel.app.views import MyBaseModelView


class CountryModelView(MyBaseModelView):
    column_list = ("name", "categories")

    column_labels = {
        "name": "Название",
        "categories": "Категории",
    }
