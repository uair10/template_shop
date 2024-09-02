from typing import Union

from pydantic.v1 import BaseModel


class Balance(BaseModel):
    currency_code: str
    available: Union[int, float]
