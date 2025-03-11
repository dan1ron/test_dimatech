"""add users and accoun

Revision ID: 75c49b9992f9
Revises: 8f27a1e1e038
Create Date: 2025-03-11 08:47:18.005189

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import Boolean, Float, Integer, String, column, or_, table

from app.api.auth import get_password_hash

# revision identifiers, used by Alembic.
revision: str = '75c49b9992f9'
down_revision: Union[str, None] = '8f27a1e1e038'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_table = table(
    'users',
    column('id', Integer),
    column('email', String),
    column('full_name', String),
    column('hashed_password', String),
    column('is_admin', Boolean),
    column('is_active', Boolean),
)

account_table = table(
    'accounts',
    column('id', Integer),
    column('balance', Float),
    column('owner_id', Integer),
)


def upgrade():
    op.bulk_insert(
        user_table,
        [
            {
                'email': 'test_admin@example.com',
                'full_name': 'Test Admin',
                'hashed_password': get_password_hash('adminpassword'),
                'is_admin': True,
                'is_active': True,
            },
            {
                'email': 'test_user@example.com',
                'full_name': 'Test User',
                'hashed_password': get_password_hash('userpassword'),
                'is_admin': False,
                'is_active': True,
            },
        ],
    )

    op.bulk_insert(
        account_table,
        [
            {
                'id': 1,
                'balance': 0.0,
                'owner_id': 2,
            }
        ],
    )


def downgrade():
    op.execute(
        user_table.delete().where(
            or_(user_table.c.email == 'test_user@example.com', user_table.c.email == 'test_admin@example.com')
        )
    )
    op.execute(account_table.delete().where(account_table.c.id == 1))