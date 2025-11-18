from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role_name: str | None = None

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
