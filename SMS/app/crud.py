from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):

    if len(user.password.encode("utf-8")) > 72:
        raise ValueError("Password too long (max 72 bytes)")

    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        email=user.email,
        password=hashed_password,
        name=user.name,
        age=user.age,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_user_todo(db: Session, user_id: int, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.model_dump(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos_by_user(db: Session, user_id: int):
    return db.query(models.Todo).filter(models.Todo.user_id == user_id).all()