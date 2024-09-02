from datetime import datetime

from pydantic.v1 import BaseModel

from .invoice import Invoice


class Update(BaseModel):
    update_id: int
    update_type: str
    request_date: datetime
    payload: Invoice
