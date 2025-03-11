from fastapi import APIRouter, HTTPException

from app.api import deps, schemas
from app.api.auth import get_password_hash
from app.database import crud

router = APIRouter()


@router.post('/users/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: deps.SessionDep, current_user: deps.CurrentUser):
    """Create new user."""
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    user.password = get_password_hash(user.password)
    return await crud.create_user(db=db, user=user)


@router.delete('/users/{user_id}', responses={404: {'model': schemas.Message}})
async def delete_user(user_id: int, db: deps.SessionDep, current_user: deps.CurrentAdminUser):
    """Delete user."""
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    await crud.delete_user(db, user_id=user_id)
    return {'message': 'User deleted'}


@router.put('/users/{user_id}', response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db: deps.SessionDep, current_user: deps.CurrentAdminUser):
    """Update user."""
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return await crud.update_user(db, user_id=user_id, user=user)


@router.get('/users/', response_model=list[schemas.User])
async def read_users(db: deps.SessionDep, current_user: deps.CurrentAdminUser):
    """Returns list of users."""
    return await crud.get_users(db)


@router.get('/users/{user_id}/accounts/', response_model=list[schemas.Account])
async def read_accounts(user_id: int, db: deps.SessionDep):
    """Returns list of accounts of user."""
    return await crud.get_accounts(db, user_id)
