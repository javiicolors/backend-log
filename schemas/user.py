# schemas/user.py
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # Cambiado de `orm_mode` a `from_attributes`

class LoginData(BaseModel):
    username: str
    password: str