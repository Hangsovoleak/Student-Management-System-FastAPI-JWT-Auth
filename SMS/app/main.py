
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, get_db, Base
from app.auth.routes import router as auth_router
from app.auth.utils import get_current_user
from . import schemas, models
from app import crud

app = FastAPI()

Base.metadata.create_all(bind=engine)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Welcome to the User Auth API"}

@app.get("/todos", response_model=list[schemas.TodoRead])
def get_my_todos(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_todos_by_user(db, user_id=current_user.id)

@app.post("/todos", response_model=schemas.TodoRead)
def create_todo(
    todo: schemas.TodoCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_user_todo(db, user_id=current_user.id, todo=todo)