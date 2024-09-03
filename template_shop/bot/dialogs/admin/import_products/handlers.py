import io

import pandas as pd
from aiogram import Bot, types
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from template_shop.bot.services.tg_helpers import answer_msg_with_autodelete
from template_shop.core.exceptions.category import CategoryIdNotExist
from template_shop.core.exceptions.country import CountryIdNotExist
from template_shop.core.utils.files import get_file_extension
from template_shop.infrastructure.database.services.product import ProductService


async def process_products_file(message: types.Message, _, manager: DialogManager):
    """Импортируем товары из эксель файла"""

    bot: Bot = manager.middleware_data.get("bot")
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    product_service: ProductService = manager.middleware_data.get("product_service")

    extension = get_file_extension(message.document.file_name)

    if extension != "xlsx":
        await answer_msg_with_autodelete(message, locale.get("wrong-file-extension"))
        return

    file = await bot.get_file(message.document.file_id)

    destination_path = io.BytesIO()
    msg = await message.answer("Обрабатываю файл")
    await bot.download_file(file.file_path, destination_path)
    excel_content = pd.read_excel(destination_path)
    excel_content.replace({pd.NA: None}, inplace=True)
    records = excel_content.to_dict(orient="records")

    created_count = 0
    for i, line in enumerate(records, start=1):
        if not line.get("product_name"):
            await message.answer(f"Не заполнено название товара в строке {i}")
            continue
        if not line.get("price"):
            await message.answer(f"Не заполнена цена в строке {i}")
            continue
        if not line.get("download_link"):
            await message.answer(f"Не заполнена ссылка на скачивание в строке {i}")
            continue
        if not line.get("category_id"):
            await message.answer(f"Не заполнен id категории в строке {i}")
            continue
        if not line.get("country_id"):
            await message.answer(f"Не заполнен id страны в строке {i}")
            continue
        if (preview_image := line.get("preview_image")) and "http" not in preview_image:
            await message.answer(f"Некорректная ссылка на фото в строке {i}")
            continue

        try:
            await product_service.create_product(
                name=line.get("product_name"),
                price=line.get("price"),
                link=line.get("download_link"),
                category_id=line.get("category_id"),
                country_id=line.get("country_id"),
                preview_image_path=preview_image,
            )
        except CountryIdNotExist:
            await message.answer(f"Страны с id {line.get('country_id')} нет в базе данных")
            continue
        except CategoryIdNotExist:
            await message.answer(f"Категории с id {line.get('category_id')} нет в базе данных")
            continue

        created_count += 1

    await msg.delete()
    await message.answer(f"Создано товаров: {created_count} из {len(records)}")

    await manager.done()
