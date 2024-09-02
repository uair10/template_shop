from datetime import datetime


def convert_float_to_str(fl: float, digits: int = 2) -> str:
    """
    Преобразуем float в строку без округления
    :param fl: Float число
    :param digits: Число знаков после точки
    :return: str
    """
    pattern = f"%.{digits}f"
    return pattern % fl


def format_date(
    my_date: datetime,
    day_format: str = "%-d",
    month_format: str = "%b.",
    year_format: str = "%Y",
):
    """Форматируем дату, подставляем суффикс"""

    date_suffixes = ["th", "st", "nd", "rd"]

    if day_format == "%-d":
        if my_date.day % 10 in [1, 2, 3] and datetime.day not in [11, 12, 13]:
            day_format = day_format + date_suffixes[my_date.day % 10]
        else:
            day_format = day_format + date_suffixes[0]
    return my_date.strftime(f"{day_format} {month_format} {year_format}")
