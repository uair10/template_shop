from aiogram_dialog import DialogManager

from template_shop.infrastructure.database.services.country import CountryService


async def countries_getter(dialog_manager: DialogManager, country_service: CountryService, **kwargs):
    countries = await country_service.get_countries()

    return {
        "countries": countries,
    }
