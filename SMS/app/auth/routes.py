from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .. import schemas, crud, database
from .utils import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


# --------------------
# SIGNUP
# --------------------
@router.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db, user=user)


# --------------------
# LOGIN
# --------------------
@router.post("/token", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = crud.get_user_by_email(db, email=form_data.username)

    if not user or not crud.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# --------------------
# CURRENT USER
# --------------------
@router.get("/me", response_model=schemas.User)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user