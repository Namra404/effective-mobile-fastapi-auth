from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.utils import decode_jwt
from app.db.databse import get_db_session
from app.models import User
from app.repositories.role_repo import RoleRepository
from app.repositories.user_repo import UserRepository
from app.repositories.access_rule_repo import AccessRoleRuleRepository
from app.services.auth_service import AuthService

from app.services.user_service import UserService
from app.services.acl_service import ACLService

http_bearer = HTTPBearer()


def get_auth_service(session: AsyncSession = Depends(get_db_session)) -> AuthService:
    user_repo = UserRepository(session)
    role_repo = RoleRepository(session)
    return AuthService(user_repo=user_repo, role_repo=role_repo)


def get_user_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserService:
    repo = UserRepository(session)
    return UserService(user_repo=repo)


def get_acl_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> ACLService:
    access_repo = AccessRoleRuleRepository(session)
    return ACLService(access_repo=access_repo)


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return payload


async def get_current_user(
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(get_db_session),
) -> User:
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return user


def get_current_active_user(
        current_user: User = Depends(get_current_user),
) -> User:
    if current_user.is_active:
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Inactive user",
    )
