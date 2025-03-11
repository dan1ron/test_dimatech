from fastapi import APIRouter

from app.api import deps, schemas
from app.database import crud

router = APIRouter()


@router.get('/users/me/', response_model=schemas.UserBase)
async def read_users_me(current_user: deps.CurrentUser):
    """Возвращает информацию о текущем авторизованном пользователе."""
    return current_user


@router.get('/users/me/accounts/', response_model=list[schemas.Account])
async def read_accounts_me(db: deps.SessionDep, current_user: deps.CurrentUser):
    """Возвращает список счетов текущего авторизованного пользователя."""
    return await crud.get_accounts(db, current_user.id)


@router.get('/users/me/payments/', response_model=list[schemas.Payment])
async def read_payments_me(db: deps.SessionDep, current_user: deps.CurrentUser):
    """Возвращает список платежей текущего авторизованного пользователя."""
    return await crud.get_payments(db, current_user.id)
