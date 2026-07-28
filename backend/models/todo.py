from datetime import datetime

from sqlalchemy import DateTime, String, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base


class Todo(Base):
    """Бд для хранения данных о самой заметке"""
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
