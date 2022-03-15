from typing import Optional

from fastapi import FastAPI, Depends, status
from sqlalchemy import desc

from models import Todos
from database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from auth import get_user_exception, get_current_user
from exceptions import http_exception


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="Priority must be between 1 and 5")
    complete: bool


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(Todos).order_by(desc(Todos.priority)).all()


@app.get("/todos/user")
async def read_all_by_user(
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user is None:
        raise get_user_exception()
    return db.query(Todos).filter(Todos.owner_id == user['id']).all()


@app.get("/todo/{todo_id}")
async def read_todo(
        todo_id: int,
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user["id"])\
        .first()
    if todo_model is not None:
        return todo_model
    raise http_exception()


@app.post("/")
async def create_todo(
        todo: Todo,
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user is None:
        raise get_user_exception()
    todo_model = Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user['id']

    db.add(todo_model)
    db.commit()

    return successful_response(status.HTTP_201_CREATED)


@app.put("/{todo_id}")
async def update_todo(
        todo_id: int,
        todo: Todo,
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(Todos).\
        filter(Todos.id == todo_id).\
        filter(Todos.owner_id == user['id']).\
        first()
    if todo_model is None:
        raise http_exception()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return successful_response(status.HTTP_200_OK)


@app.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(Todos).\
        filter(Todos.id == todo_id).\
        first()
    if todo_model is None:
        raise http_exception()
    db.query(Todos).\
        filter(Todos.id == todo_id).\
        delete()
    db.commit()

    return successful_response(status.HTTP_200_OK)


def successful_response(status_code: int):
    return {
        "status_code": status_code,
        "transaction": "Successful"
    }
