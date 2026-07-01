

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
from enum import Enum


class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class StudentBase(BaseModel):
    gender: Optional[GenderEnum] = GenderEnum.other
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None
    course: Optional[str] = None
    gpa: Optional[str] = None
    is_active: Optional[bool] = True

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    name: str
    age: int

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    todos: List[TodoRead] = Field(default_factory=list)

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None