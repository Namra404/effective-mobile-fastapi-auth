from fastapi import APIRouter, Depends, status, Form

from app.auth.utils import encode_jwt
from app.routes.dependencies import get_auth_service
from app.routes.mapper import user_to_schema
from app.schemas.auth import TokenInfo, RegisterRequest
from app.models import User
from app.schemas.users import UserBase
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


async def validate_auth_user(
        email: str = Form(...),
        password: str = Form(...),
        auth_service: AuthService = Depends(get_auth_service),
) -> User:
    user = await auth_service.authenticate(
        email=email,
        password=password,
    )
    return user


@router.post(path="/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
        user: User = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
        "is_active": user.is_active,
        "role": user.role.name if getattr(user, "role", None) else None,
    }

    token = encode_jwt(jwt_payload)

    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )

@router.post(
    path="/register/",
    response_model=UserBase,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
        payload: RegisterRequest,
        auth_service: AuthService = Depends(get_auth_service),
):
    user = await auth_service.register(payload)
    return user_to_schema(user)
