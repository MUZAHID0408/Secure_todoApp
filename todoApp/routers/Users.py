from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from model import Users
from database import sessionLocal
from routers.auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags= ['users']
)


def get_db():
    db = sessionLocal()
    try:
        yield db

    finally:
        db.close()


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)





db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

@router.get('/active_user', status_code=status.HTTP_200_OK)
async def get_current_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Authentication failed"
        )
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_dict = user_model.__dict__

    user_dict.pop('hashed_password', None)

    return user_dict


@router.post('/change_password', status_code=status.HTTP_201_CREATED)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Authentication failed"
        )

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    if not bcrypt_context.verify(user_verification.password, str(user_model.hashed_password)):
        raise HTTPException(
            status_code=401,
            detail="Password didn't match verification failed!"
        )
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


