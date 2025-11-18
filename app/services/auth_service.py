from fastapi import HTTPException, status

from app.auth.utils import hash_password, validate_password
from app.models import User
from app.repositories.role_repo import RoleRepository
from app.repositories.user_repo import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest


class AuthService:
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository) -> None:
        self.user_repo = user_repo
        self.role_repo = role_repo

    async def register(self, payload: RegisterRequest) -> User:
        if payload.password != payload.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match",
            )

        existing = await self.user_repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        raw_hash: bytes = hash_password(payload.password)
        hashed_str = raw_hash.decode()

        user_role = await self.role_repo.get_by_name("user")
        role_id = user_role.id if user_role else None

        user = await self.user_repo.create(
            email=payload.email,
            hashed_password=hashed_str,
            first_name=payload.first_name,
            last_name=payload.last_name,
            patronymic=payload.patronymic,
            role_id=role_id,
        )
        return user

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        hashed_from_db = user.hashed_password
        if isinstance(hashed_from_db, str):
            hashed_from_db = hashed_from_db.encode()

        if not validate_password(
                password=password,
                hashed_password=hashed_from_db,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        return user

    async def authenticate_request(self, payload: LoginRequest) -> User:

        password_str = payload.password.decode()
        return await self.authenticate(email=payload.email, password=password_str)
