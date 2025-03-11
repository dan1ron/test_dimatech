from urllib.parse import quote

import pydantic
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict



class Postgres(pydantic.BaseModel):
    host: str
    port: int
    user: str
    password: str
    db: str
    print_sql: bool = False

    @computed_field
    @property
    def url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme='postgresql+asyncpg',
                username=quote(self.user),
                password=quote(self.password),
                host=self.host,
                port=self.port,
                path=self.db,
            )
        )


class JWT(pydantic.BaseModel):
    algorithm: str = 'HS256'
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class AppSettings(BaseSettings):
    signature_secret_key: str
    postgres: Postgres
    jwt: JWT

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
        extra='ignore',
    )


settings = AppSettings()
