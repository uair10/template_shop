import io
from typing import Any

import openpyxl

from template_shop.infrastructure.database.models import Product


def get_excel_values(product: Product) -> dict[str, Any]:
    return {
        "Document name": product.name,
        "Download link": product.link,
    }


def export_products_to_xlsx(
    products: list[Product],
) -> bytes:
    output = io.BytesIO()
    wb = openpyxl.Workbook()
    excel_values = get_excel_values(products[0])
    try:
        ws = wb.active
        ws.append(list(excel_values.keys()))
        for product in products:
            excel_values = get_excel_values(product)
            ws.append(list(excel_values.values()))
        wb.save(output)
    finally:
        wb.close()
    output.seek(0)
    return output.read()
