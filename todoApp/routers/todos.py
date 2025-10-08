from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from model import Todos, Users
from database import sessionLocal
from routers.auth import get_current_user

router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db

    finally:
        db.close()

#BaseModel template for inserting Todos
class TodosRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    Priority: int = Field(gt = 0)
    Complete: bool



db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/')
async def read_default(user: user_dependency, db: db_dependency):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )

    return db.query(Todos).filter(Todos.user == user.get('id')).all()




@router.get("/todo/{todo_id}", status_code = status.HTTP_200_OK)
async def read_todo_with_id(owner : user_dependency,db : db_dependency, todo_id : int = Path(gt=0)):

    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )

    todo_info = db.query(Todos).filter(Todos.ID == todo_id).filter(Todos.user == owner.get('id')).first()
    if todo_info is not None:
        return todo_info
    raise HTTPException(status_code = 404, detail = 'Todos not found with that ID')


@router.post("/todo/insert", status_code=status.HTTP_201_CREATED)
async def create_todo(owner: user_dependency, db:db_dependency, todo_request: TodosRequest):

    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )

    todo_request = Todos(**todo_request.model_dump(), user = owner.get('id') )
    db.add(todo_request)
    db.commit()


@router.put("/todo/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,db:db_dependency, todo_request: TodosRequest, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )

    todo_model_from_db = db.query(Todos).filter(Todos.ID == todo_id).filter(Todos.user == user.get('id')).first()

    #check if its emtpy
    if todo_model_from_db is None:
        raise HTTPException(status_code=404, detail="No Todos found with this ID")


    #if not raise condition occurrence then this  code will run, will not run otherwise
    todo_model_from_db.title = todo_request.title
    todo_model_from_db.description = todo_request.description
    todo_model_from_db.Priority = todo_request.Priority
    todo_model_from_db.Complete = todo_request.Complete

    #add the same todo_model grabbed from the database with changes.
    db.add(todo_model_from_db)
    db.commit()


@router.delete("/todo/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db:db_dependency, todo_id: int = Path(gt = 0)):


    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )

    todo_model_from_db = db.query(Todos).filter(Todos.ID == todo_id).filter(Todos.user == user.get('id')).first()

    # check if its emtpy
    if todo_model_from_db is None:
        raise HTTPException(status_code=404, detail="No Todos found with this ID")
    db.query(Todos).filter(Todos.ID == todo_id).delete()
    db.commit()







