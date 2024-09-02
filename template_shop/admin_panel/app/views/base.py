from template_shop.admin_panel.app.views.admin_lte import AdminLTEModelView
from template_shop.admin_panel.app.views.mixins import AuthMixin


class MyBaseModelView(AuthMixin, AdminLTEModelView):
    page_size = 10
    edit_modal = True
    column_display_pk = True
    create_modal = True
    can_export = True
    can_view_details = True
    column_hide_backrefs = False
    details_modal = True
    can_set_page_size = True

    export_types = ["xlsx", "csv"]

    form_excluded_columns = ("created_at", "updated_at")

    column_labels = {
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
    }
