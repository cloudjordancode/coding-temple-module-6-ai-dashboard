# project/starter/app/routers/auth.py
# Module 5 Project — Auth endpoints
#
# TODO: Implement POST /register, POST /token, GET /me

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.database import get_db
from app.models.user import User
from app.auth import hash_password, verify_password, create_access_token, get_current_user


router = APIRouter()


# TODO: POST /register
@router.post("/register", response_model=TokenResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return a token."""
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer"}


# TODO: POST /token
@router.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Log in and receive an access token."""

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# TODO: GET /me
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):  # TODO: replace None
    """Return the authenticated user's profile."""
    return current_user
