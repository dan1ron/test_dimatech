from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import create_engine

from app.conf import settings

# https://github.com/sqlalchemy/sqlalchemy/discussions/10246
engine = AsyncEngine(
    create_engine(
        settings.postgres.url,
        echo=settings.postgres.print_sql,
        future=True,
        poolclass=pool.NullPool,
        connect_args={
            'statement_cache_size': 0,
            'prepared_statement_name_func': lambda: '',
            'prepared_statement_cache_size': 0,
            'server_settings': {
                'application_name': 'smartcity-reports-generator',
            },
        },
    )
)
