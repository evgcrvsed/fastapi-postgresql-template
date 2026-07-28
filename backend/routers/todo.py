from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import TodoUpdate, TodoResponse, TodoCreate
from backend.services import TodoService

router = APIRouter(prefix="/api/todos", tags=["todos"])

DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=list[TodoResponse])
async def list_of_todos(db: DbDep):
    return await TodoService(db).list_all()

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(data: TodoCreate, db: DbDep):
    return await TodoService(db).create(data.text)

@router.patch("/", response_model=TodoResponse)
async def update_todo(data: TodoUpdate, db: DbDep):
    todo = await TodoService(db).update_by_text(data.text, data.finished)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo
