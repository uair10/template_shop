from typing import Any

from aiogram import F
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format

from template_shop.bot.dialogs.widgets import LocaleText, StartWithData
from template_shop.bot.states import OrderDetailsSG, PaymentSG, PromocodeSG
from template_shop.bot.states.user import BuyAccountSG

from ...getters.cart import cart_getter
from ...getters.categories import categories_getter
from ...getters.countries import countries_getter
from ...getters.orders import order_summary_getter
from ...getters.product import product_info_getter, products_getter
from .handlers import (
    add_product_to_cart,
    clear_cart,
    create_order,
    order_doc_drawing,
    select_product,
    set_category_id,
    set_country_id,
    set_template_type,
)


async def on_process_result(_, result: Any, manager: DialogManager):
    """Добавляем результат вложенного диалога в текущий"""

    ctx = manager.current_context()
    if result and isinstance(result, dict):
        ctx.dialog_data.update(result)


select_template_type_window = Window(
    LocaleText("select-template-type-msg"),
    Button(LocaleText("documents-btn"), "documents", on_click=set_template_type),
    Button(LocaleText("cards-btn"), "cards", on_click=set_template_type),
    Cancel(LocaleText("back-btn")),
    state=BuyAccountSG.select_template_type,
)

select_country_window = Window(
    LocaleText("select-country-msg"),
    ScrollingGroup(
        Select(
            Format("{item.name}"),
            "countries_sel",
            lambda country: country.id,
            "countries",
            on_click=set_country_id,
        ),
        width=3,
        height=4,
        id="countriessel",
        hide_on_single_page=True,
    ),
    Back(LocaleText("back-btn")),
    state=BuyAccountSG.select_country,
    getter=countries_getter,
)


select_category_window = Window(
    LocaleText("select-category-msg"),
    ScrollingGroup(
        Select(
            Format("{item.name}"),
            "categories_sel",
            lambda category: category.id,
            "categories",
            on_click=set_category_id,
        ),
        width=3,
        height=4,
        id="categoriesssel",
        hide_on_single_page=True,
    ),
    Back(LocaleText("back-btn")),
    state=BuyAccountSG.select_category,
    getter=categories_getter,
)

select_products_window = Window(
    LocaleText(
        "select-products-msg",
    ),
    LocaleText("cart-total", cart_total="{cart_total}"),
    ScrollingGroup(
        Select(
            Format("{item.name} {item.price}$"),
            "products_sel",
            lambda product: product.id,
            "products",
            on_click=select_product,
        ),
        width=1,
        height=4,
        id="categoriesssel",
        hide_on_single_page=True,
    ),
    SwitchTo(LocaleText("confirm-btn"), "confirm_btn", BuyAccountSG.overview_order, when=F["cart_total"] > 0),
    Button(LocaleText("clear-cart-btn"), "clear_cart", on_click=clear_cart),
    SwitchTo(LocaleText("back-btn"), "back_btn", BuyAccountSG.select_template_type, when=F["template_type"] == "cards"),
    Back(LocaleText("back-btn"), when=F["template_type"] != "cards"),
    state=BuyAccountSG.select_products,
    getter=(products_getter, cart_getter),
)

product_info_window = Window(
    LocaleText("product-title", product_title="{product_title}"),
    LocaleText("product-price", product_price="{product_price}"),
    DynamicMedia(
        "product_preview_img",
        when=F["product_preview_img"],
    ),
    Button(LocaleText("add-to-cart-btn"), "add_to_cart", on_click=add_product_to_cart),
    Button(LocaleText("order-doc-drawing-btn"), "doc_drawing", on_click=order_doc_drawing),
    Back(LocaleText("back-btn")),
    state=BuyAccountSG.product_info,
    getter=product_info_getter,
)

overview_order_window = Window(
    LocaleText("order-overview"),
    Format("{order_products}"),
    LocaleText("order-summ", order_summ="{order_summ}"),
    LocaleText("discount-summ", discount_summ="{discount_summ}", when=F["discount_summ"]),
    StartWithData(
        LocaleText("add-balance-btn"),
        id="add_balance_btn",
        state=PaymentSG.select_method,
        data_keys=["order_summ"],
    ),
    StartWithData(
        LocaleText("enter-promocode-btn"),
        id="enter_promocode_btn",
        state=PromocodeSG.enter_promocode,
        data_keys=["order_summ"],
    ),
    Button(
        LocaleText("confirm-btn"),
        id="confirm_order_button",
        on_click=create_order,
    ),
    SwitchTo(LocaleText("back-btn"), "back_btn", BuyAccountSG.select_products),
    state=BuyAccountSG.overview_order,
    getter=order_summary_getter,
)

order_created_window = Window(
    LocaleText(
        "order-created-msg",
    ),
    StartWithData(
        LocaleText("go-to-order-btn"),
        id="go_to_order_btn",
        state=OrderDetailsSG.order_details,
        data_keys=["order_id"],
    ),
    Cancel(LocaleText("main-menu-btn")),
    state=BuyAccountSG.order_created,
)

create_order_dialog = Dialog(
    select_template_type_window,
    select_country_window,
    select_category_window,
    select_products_window,
    product_info_window,
    overview_order_window,
    order_created_window,
    on_process_result=on_process_result,
)
