from typing import Iterable

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..api import schemas
from . import models


async def get_user(db: AsyncSession, user_id: int) -> models.User | None:
    query = select(models.User).where(models.User.id == user_id)
    return (await db.exec(query)).first()


async def get_users(db: AsyncSession) -> Iterable[models.User]:
    query = select(models.User)
    return (await db.exec(query)).all()


async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    query = select(models.User).where(models.User.email == email)
    return (await db.exec(query)).first()


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    db_user = models.User(email=user.email, full_name=user.full_name, hashed_password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user: schemas.User) -> models.User:
    db_user = await db.get(models.User, user_id)
    for field, value in user.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await db.get(models.User, user_id)
    await db.delete(db_user)
    await db.commit()


async def get_accounts(db: AsyncSession, user_id: int) -> Iterable[models.Account]:
    query = select(models.Account).where(models.Account.owner_id == user_id)
    return (await db.exec(query)).all()


async def create_account(db: AsyncSession, user_id: int) -> models.Account:
    db_account = models.Account(owner_id=user_id)
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account


async def get_payments(db: AsyncSession, user_id: int) -> Iterable[models.Payment]:
    query = select(models.Payment).where(models.Payment.user_id == user_id)
    return (await db.exec(query)).all()


async def create_payment(db: AsyncSession, payment: schemas.Payment):
    account_query = select(models.Account).where(models.Account.owner_id == payment.user_id)
    account = (await db.exec(account_query)).first()
    if not account:
        account = models.Account(owner_id=payment.user_id, balance=0.0)
        db.add(account)
        await db.commit()
        await db.refresh(account)

    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)

    account.balance += payment.amount

    await db.commit()
    await db.refresh(db_payment)
    await db.refresh(account)

    return db_payment


async def get_payment_by_transaction_id(db: AsyncSession, transaction_id: str) -> models.Payment | None:
    query = select(models.Payment).where(models.Payment.transaction_id == transaction_id)
    return (await db.exec(query)).first()
