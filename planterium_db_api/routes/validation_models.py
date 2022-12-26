from pydantic import BaseModel, ValidationError


class BotAdmin(BaseModel):
    user_id: int
