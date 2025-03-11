import uuid
from typing import List

import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int = Field(primary_key=True)
    email: str = Field(sa_type=sa.String, unique=True, index=True)
    full_name: str = Field(sa_type=sa.String(128))
    hashed_password: str = Field(sa_type=sa.String(128))
    is_admin: bool = Field(sa_type=sa.Boolean, default=False)
    is_active: bool = Field(sa_type=sa.Boolean, default=True)

    accounts: List['Account'] = Relationship(back_populates='owner')
    payments: List['Payment'] = Relationship(back_populates='user')


class Account(SQLModel, table=True):
    __tablename__ = 'accounts'

    id: int = Field(sa_type=sa.Integer, primary_key=True, index=True)
    balance: float = Field(sa_type=sa.Float, default=0.0)
    owner_id: int = Field(sa_type=sa.Integer, foreign_key='users.id')

    owner: User = Relationship(back_populates='accounts')


class Payment(SQLModel, table=True):
    __tablename__ = 'payments'

    id: int = Field(sa_type=sa.Integer, primary_key=True, index=True)
    transaction_id: uuid.UUID = Field(sa_type=sa.UUID, unique=True)
    amount: float = Field(sa_type=sa.Float)
    user_id: int = Field(sa_type=sa.Integer, foreign_key='users.id')

    user: User = Relationship(back_populates='payments')
