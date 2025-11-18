from app.models import User
from app.schemas.users import UserBase


def user_to_schema(user: User) -> UserBase:
    return UserBase(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        role_name=user.role.name if getattr(user, "role", None) else None,
    )
