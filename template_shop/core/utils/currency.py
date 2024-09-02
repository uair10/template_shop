import logging

from aiohttp import ClientSession

logger = logging.getLogger(__name__)


async def get_rate_usd() -> float:
    """Получаем курс доллара"""

    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        async with ClientSession() as session:
            async with session.get(url, verify_ssl=False) as req_:
                res = await req_.json(content_type=None)
        return res.get("Valute").get("USD").get("Value")
    except Exception as e:
        logger.exception(e)
        return 0
