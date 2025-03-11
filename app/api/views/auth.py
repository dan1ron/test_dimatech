from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from app.api import deps, schemas
from app.api.auth import authenticate_user, create_access_token, get_email_from_access_token
from app.conf import settings
from app.database import crud

router = APIRouter()


@router.post('/token', response_model=schemas.ResponseAccessTokenWithRefreshToken)
async def login_for_access_token(
    db: deps.SessionDep,
    form_data: schemas.UserLogin,
):
    user = await authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(data={'sub': user.email})
    refresh_token = create_access_token(
        data={'sub': user.email}, expires_delta=timedelta(days=settings.jwt.refresh_token_expire_days)
    )
    return schemas.ResponseAccessTokenWithRefreshToken(access_token=access_token, refresh_token=refresh_token)


@router.post('/refresh-token', response_model=schemas.ResponseAccessToken)
async def refresh_token(refresh_token: str, db: deps.SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    email = get_email_from_access_token(refresh_token)
    if email is None:
        raise credentials_exception

    user = await crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    access_token = create_access_token(data={'sub': user.email})
    return schemas.ResponseAccessToken(access_token=access_token)
