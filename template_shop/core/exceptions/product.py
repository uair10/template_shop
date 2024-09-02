from dataclasses import dataclass

from template_shop.core.exceptions.common import ApplicationException


@dataclass
class ProductIdNotExist(ApplicationException):
    product_id: int

    @property
    def message(self) -> str:
        return f"Product with id {self.product_id} doesn't exists"
