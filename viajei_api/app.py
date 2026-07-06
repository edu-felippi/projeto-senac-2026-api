from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from viajei_api.database import get_session
from viajei_api.models import User
from viajei_api.schemas.message import Message
from viajei_api.schemas.token import Token
from viajei_api.schemas.user import UserList, UserPublic, UserSchema
from viajei_api.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)

app = FastAPI()

database = []

origins = [
    "http://localhost:3000",
    "htpp://127.0.0.1:3000",
    "http://localhost:5000",
    "htpp://127.0.0.1:5000",
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"funcionou": "(/◕ヮ◕)/"}


@app.get("/hello", response_class=HTMLResponse)
def hello_world():
    return """
    <html>
        <head>
            <title> Hello World! </title>
        </head>
        <body>
            <h1>Olá mundo!</h1>
        </body>
    </html>"""


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where((User.email == user.email)))

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="This email already exists",
        )

    hashed_password = get_password_hash(user.password)

    db_user = User(email=user.email, password=hashed_password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users/", response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    session.delete(db_user)
    session.commit()

    return {"message": "User deleted"}


@app.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    return database[user_id - 1]


@app.post("/auth", response_model=Token)
def retrieve_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
