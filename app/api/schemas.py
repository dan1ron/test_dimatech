from pydantic import BaseModel, EmailStr, create_model


class Forbidden(BaseModel):
    detail: str


class BadRequest(BaseModel):
    detail: str


class Unauthorized(BaseModel):
    detail: str


class UserBase(BaseModel):
    id: int = None
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    is_active: bool
    is_admin: bool


# Создаем новую модель с опциональными полями
UserUpdate = create_model(
    'UserUpdate',
    __base__=User,
    **{field: (field_type.annotation, None) for field, field_type in User.__pydantic_fields__.items()}
)


class UserLogin(BaseModel):
    email: str
    password: str


class Account(BaseModel):
    id: int
    owner_id: int
    balance: float


class Payment(BaseModel):
    id: int = None
    user_id: int
    account_id: int
    transaction_id: str
    amount: float
    signature: str


class ResponseAccessToken(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class ResponseAccessTokenWithRefreshToken(ResponseAccessToken):
    refresh_token: str


class Message(BaseModel):
    detail: str
