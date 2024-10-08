from pydantic.v1 import BaseModel


class Profile(BaseModel):
    app_id: int
    name: str
    payment_processing_bot_username: str
