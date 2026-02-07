from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.api.deps import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.db.models import User
from app.schemas.auth import UserCreate, UserRead, Token

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, session: Session = Depends(get_db)):
    existing = session.exec(
        select(User).where((User.email == user_in.email) | (User.username == user_in.username))
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    user = User(
        username=user_in.username,
        email=user_in.email,
        passwordhash=hash_password(user_in.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    # form_data.username -> email (PRD me email unique hai) [file:4]
    user = session.exec(
        select(User).where(User.email == form_data.username)
    ).first()
    if not user or not verify_password(form_data.password, user.passwordhash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
