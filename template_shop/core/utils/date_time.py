from datetime import datetime

from pytz import timezone


def get_date_time(tz: str = "Europe/Moscow", time_format="%Y-%m-%d %H:%M:%S", as_string: bool = False):
    """Получаем текущую дату и время"""

    date_and_time = datetime.now(timezone(tz)).replace(tzinfo=None).replace(microsecond=0)

    if as_string:
        date_and_time = date_and_time.strftime(time_format)

    return date_and_time
