import json
from datetime import datetime, timedelta

import pandas as pd
from flask import jsonify, request
from flask_admin import AdminIndexView, expose
from sqlalchemy import func, select

from template_shop.admin_panel.app import db
from template_shop.admin_panel.app.views.mixins import AuthMixin
from template_shop.infrastructure.database.services.statistics import Statistics


class MyAdminIndexView(AuthMixin, AdminIndexView):
    @staticmethod
    def get_chart_data(date_from: datetime = None, period: int = 31):
        if not date_from:
            date_from = datetime.now().date() - timedelta(days=period)

        dates = []
        products_purchased = []
        registered_users = []
        orders_created = []
        payments_payed = []

        for i in range(0, period + 1):
            current_date = date_from + timedelta(days=i)
            dates.append(current_date.strftime("%Y-%m-%d"))

            statistics = db.session.execute(
                select(Statistics).where(func.date(Statistics.date) == current_date),
            ).scalar()

            products_purchased.append(statistics.products_purchased if statistics else 0)
            registered_users.append(statistics.users_registered if statistics else 0)
            orders_created.append(statistics.orders_created if statistics else 0)
            payments_payed.append(statistics.payments_payed if statistics else 0)

        data = {
            "products_purchased": products_purchased,
            "registered_users": registered_users,
            "orders_created": orders_created,
            "payments_payed": payments_payed,
        }

        df = pd.DataFrame(data, index=dates)
        pd.options.display.float_format = "{:,.0f}".format
        df = df.loc[:, df.columns != "labels"]
        df.loc[len(df)] = df.sum(axis=0)
        if df.isnull().values.any():
            df.fillna(0, inplace=True)
        table_rows = df[0:-1].astype(int).values.tolist()
        rows_sums = df.iloc[-1].astype(int).values.tolist()

        data.update(
            {
                "dates": json.dumps(dates),
                "table_rows": table_rows,
                "rows_sums": rows_sums,
            },
        )

        return dates, data, table_rows, rows_sums

    @expose("/", methods=["GET", "POST"])
    def index(self):
        if request.method == "POST":
            try:
                date_from = datetime.strptime(request.form.get("date_from"), "%Y-%m-%d")
                date_to = datetime.strptime(request.form.get("date_to"), "%Y-%m-%d")
                period = abs(date_to - date_from).days
                data = self.get_chart_data(date_from, period)
                return jsonify(data)
            except ValueError:
                return ("", 204)
        else:
            dates, data, table_rows, rows_sums = self.get_chart_data()
            return self.render(
                "myadmin3/my_index.html",
                data=data,
                dates=dates,
                table_columns=zip(dates, table_rows),
            )
