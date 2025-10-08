from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database import sessionLocal
from model import Users
from jose import jwt, JWTError

bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
Oauth2_Bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
router = APIRouter(
    prefix='/auth',
    tags = ['auth']
)

#secret key for json web token
SECRET_KEY = "01f0401b1a86acfaf40e7107fa27bbfc687e9b95649eb23573a9c6191624bd95"

#Algorithm used
ALGORITHM = "HS256"

class CreateUser(BaseModel):
    email : str
    username : str
    firstname : str
    lastname : str
    password : str
    is_active : bool
    role : str

class Token(BaseModel):
    access_token : str
    token_type: str


def get_db():
    db = sessionLocal()
    try:
        yield db

    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username ==  username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expeire_time: timedelta):
    total_time = datetime.now(timezone.utc) + expeire_time
    encode = {"sub": username, "id": user_id, "role": role , "exp":total_time}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(Oauth2_Bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role : str = payload.get('role')
        if user_name is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user'
            )

        return {'user': user_name, 'id': user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )



@router.post("/", status_code= status.HTTP_201_CREATED)
async def create_user(db : db_dependency ,create_new_user: CreateUser):
    try:
        create_user_model = Users(
            email = create_new_user.email,
            username=create_new_user.username,
            firstname=create_new_user.firstname,
            lastname = create_new_user.lastname,
            hashed_password=bcrypt_context.hash(create_new_user.password),
            is_active=True,
            role = create_new_user.role
        )

        db.add(create_user_model)
        db.commit()

        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Internal server error,{str(e)} '
        )


@router.post('/token', status_code=status.HTTP_201_CREATED, response_model = Token)
async def get_login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency ):

    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            return "Login failed.. try again."
        token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

        return {
            "access_token" : token,
            "token_type" : "bearer"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Internal server error: {str(e)}'
        )



