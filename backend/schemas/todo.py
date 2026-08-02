from datetime import datetime

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class TodoUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=1, max_length=1000)
    finished: bool | None = None


class TodoResponse(BaseModel):
    id: int
    text: str
    finished: bool
    created_at: datetime

    model_config = {"from_attributes": True}
