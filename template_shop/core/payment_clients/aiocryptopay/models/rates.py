from typing import Union

from pydantic.v1 import BaseModel


class ExchangeRate(BaseModel):
    is_valid: bool
    source: str
    target: str
    rate: Union[int, float]
