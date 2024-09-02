from strenum import StrEnum


class HTTPMethods(StrEnum):
    """Available HTTP methods."""

    POST = "POST"
    GET = "GET"


class Networks(StrEnum):
    """Cryptobot networks"""

    MAIN_NET = "https://pay.crypt.bot"
    TEST_NET = "https://testnet-pay.crypt.bot"


class Assets(StrEnum):
    """Cryptobot assets"""

    BTC = "BTC"
    TON = "TON"
    ETH = "ETH"
    USDT = "USDT"
    USDC = "USDC"
    BUSD = "BUSD"
    BNB = "BNB"
    TRX = "TRX"

    @classmethod
    def values(cls):
        return [asset.value for asset in cls]


class PaidButtons(StrEnum):
    """Cryptobot paid button names"""

    VIEW_ITEM = "viewItem"
    OPEN_CHANNEL = "openChannel"
    OPEN_BOT = "openBot"
    CALLBACK = "callback"


class InvoiceStatus(StrEnum):
    """Invoice status"""

    ACTIVE = "active"
    PAID = "paid"
    EXPIRED = "expired"
