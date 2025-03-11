from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.api import deps
from app.conf import settings
from app.database import crud, models

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(db: deps.SessionDep, email: str, password: str) -> Optional[models.User]:
    user = await crud.get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT токен."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt.access_token_expire_minutes)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
    return encoded_jwt


def get_email_from_access_token(access_token: str) -> Optional[str]:
    try:
        payload = jwt.decode(access_token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        email: str = payload.get('sub')
        if email is None:
            return None
        expire = payload.get('exp')
        if expire is None or datetime.utcnow() > datetime.fromtimestamp(expire):
            return None
        return email
    except JWTError:
        return None
