from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Todo


class TodoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self) -> list[Todo]:
        result = await self.db.execute(select(Todo).order_by(Todo.id))
        return list(result.scalars().all())

    async def create(self, text: str) -> Todo:
        todo = Todo(text=text)
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        return todo

    async def update_by_text(self, text: str, finished: bool) -> Todo | None:
        result = await self.db.execute(select(Todo).where(Todo.text == text))
        todo: Todo = result.scalar_one_or_none()

        if todo is None:
            return None

        todo.finished = finished
        await self.db.commit()
        await self.db.refresh(todo)
        return todo