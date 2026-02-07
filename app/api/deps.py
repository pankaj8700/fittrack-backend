from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session, select

from app.core.config import settings
from app.db.session import get_session
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def get_db(session: Session = Depends(get_session)):
    return session


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    user = session.exec(select(User).where(User.id == int(user_id))).first()
    if not user:
        raise credentials_exc
    return user
