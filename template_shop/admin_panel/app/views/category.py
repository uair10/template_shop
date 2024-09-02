from template_shop.admin_panel.app.views import MyBaseModelView


class CategoryModelView(MyBaseModelView):
    column_list = ("name", "price")

    column_labels = {
        "name": "Название",
        "price": "Цена",
        "products": "Товары",
    }
