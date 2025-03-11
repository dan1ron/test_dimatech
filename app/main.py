import logging.config
from typing import Literal

from fastapi import FastAPI

from .api import schemas
from .api.views import admin_router, auth_router, payments_router, users_router

logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {'console': {'class': 'logging.StreamHandler'}},
        'loggers': {'app': {'handlers': ['console'], 'level': 'INFO', 'propagate': False}},
    }
)

app = FastAPI(
    title='ReportService',
    openapi_url='/api/v1/openapi.json',
    swagger_ui_parameters={'syntaxHighlight.theme': 'obsidian'},
    responses={
        401: {'description': 'Auth info is missing or invalid', 'model': schemas.Unauthorized},
        403: {'description': 'Not enough privileges', 'model': schemas.Forbidden},
        500: {'description': 'Internal server error'},
    },
)

app.include_router(auth_router, prefix='/api/v1/auth')
app.include_router(users_router, prefix='/api/v1')
app.include_router(admin_router, prefix='/api/v1')
app.include_router(payments_router, prefix='/api/v1/payments')


@app.get('/health_check', include_in_schema=False)
async def health_check() -> Literal['ok']:
    return 'ok'
