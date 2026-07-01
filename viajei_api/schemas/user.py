from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    email: EmailStr
    id: int


class UserDB(User):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
