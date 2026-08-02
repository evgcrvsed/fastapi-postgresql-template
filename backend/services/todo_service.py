from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Todo
from backend.schemas import TodoUpdate


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

    async def update(self, todo_id: int, data: TodoUpdate) -> Todo | None:
        todo = await self.db.get(Todo, todo_id)
        if todo is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(todo, field, value)

        await self.db.commit()
        await self.db.refresh(todo)
        return todo

    async def delete(self, todo_id: int) -> bool:
        todo = await self.db.get(Todo, todo_id)
        if todo is None:
            return False

        await self.db.delete(todo)
        await self.db.commit()
        return True
