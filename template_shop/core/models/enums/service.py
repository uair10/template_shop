import enum


class ServiceType(enum.Enum):
    certificate = "Сертификат"
    declaration = "Декларация"
    declaration_gost = "Декларация ГОСТ"
    letter = "Отказное письмо"
    sgr = "СГР (Свидетельство о гос. регистрации)"
    sgr_declaration = "СГР + Декларация"
    ru = "РУ (Регистрационное удостоверение)"

    @classmethod
    def choices(cls):
        return [(choice, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self) -> str:
        return str(self.value)
