from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine

import models
import config
from exceptions import token_exception, get_user_exception


class CreateUser(BaseModel):
    username: str
    email: Optional[EmailStr]
    first_name: str
    last_name: str
    password: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_passowrd, hashed_password):
    return bcrypt_context.verify(plain_passowrd, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).\
        filter(models.Users.username == username).\
        first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
        username: str,
        user_id: int,
        expires_delta: Optional[timedelta] = None
):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if not username or not user_id:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


@app.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.Users()
    create_user_model.username = create_user.username
    create_user_model.email = create_user.email
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name

    hash_password = get_password_hash(create_user.password)

    create_user_model.hashed_password = hash_password
    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()

    return {
        "status": status.HTTP_201_CREATED,
        "transaction": "Successful"
    }


@app.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()

    token = create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=timedelta(minutes=20)
    )
    return {"token": token}
