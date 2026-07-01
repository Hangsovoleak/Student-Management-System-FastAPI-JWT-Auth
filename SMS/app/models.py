

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class GenderEnum(str, enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    name = Column(String(255))
    age = Column(Integer)
    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255))
     #foreign key to user
    user_id = Column(Integer, ForeignKey('users.id')) # ensure this exists

    owner = relationship("User", back_populates="todos")

    # student-related fields
    gender = Column(Enum(GenderEnum), default=GenderEnum.other)
    date_of_birth = Column(Date)
    phone_number = Column(String(255))
    address = Column(Text)
    enrollment_date = Column(Date)
    course = Column(String(255))
    gpa = Column(String(5)) # can use float/decimal if you prefer precision
    is_active = Column(Boolean, default=True)