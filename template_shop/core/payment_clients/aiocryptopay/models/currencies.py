from typing import Optional

from pydantic.v1 import BaseModel


class Currency(BaseModel):
    is_blockchain: bool
    is_stablecoin: bool
    is_fiat: bool
    name: str
    code: str
    url: Optional[str]
    decimals: int
