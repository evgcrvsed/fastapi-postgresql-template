from datetime import datetime
from pydantic import BaseModel


class TodoCreate(BaseModel):
    text: str

class TodoUpdate(BaseModel):
    text: str
    finished: bool

class TodoResponse(BaseModel):
    id: int
    text: str
    finished: bool
    created_at: datetime

    model_config = {"from_attributes": True}