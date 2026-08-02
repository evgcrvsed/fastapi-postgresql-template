from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import TodoCreate, TodoResponse, TodoUpdate
from backend.services import TodoService

router = APIRouter(prefix="/api/todos", tags=["todos"])

DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=list[TodoResponse])
async def list_of_todos(db: DbDep):
    return await TodoService(db).list_all()


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(data: TodoCreate, db: DbDep):
    return await TodoService(db).create(data.text)


@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, data: TodoUpdate, db: DbDep):
    todo = await TodoService(db).update(todo_id, data)
    if todo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: DbDep):
    if not await TodoService(db).delete(todo_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Todo not found")
