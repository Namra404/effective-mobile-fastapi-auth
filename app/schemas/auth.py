from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: bytes


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    password: str
    password_confirm: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
