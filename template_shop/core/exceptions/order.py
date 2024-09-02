from dataclasses import dataclass

from template_shop.core.exceptions.common import BaseTgException


@dataclass
class OrderIdNotExist(BaseTgException):
    msg_for_user: str = "order-not-exists-msg"


@dataclass
class OrderIdAlreadyExist(BaseTgException):
    msg_for_user: str = "order-already-exists-msg"
