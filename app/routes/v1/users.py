from fastapi import APIRouter, Depends, status

from app.core.enums import BusinessElementEnum
from app.models.user import User
from app.routes.dependencies import get_current_active_user, get_user_service, get_acl_service
from app.schemas.users import UserBase, UserUpdateRequest
from app.services.acl_service import ACLService

from app.services.user_service import UserService

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@router.get("/me")
async def get_me(
        current_user: User = Depends(get_current_active_user),
        user_service: UserService = Depends(get_user_service),
):
    """
    Информация о текущем пользователе.
    """
    user = await user_service.get_me(current_user)
    return user


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: int,
        current_user: User = Depends(get_current_active_user),
        user_service: UserService = Depends(get_user_service),
        acl_service: ACLService = Depends(get_acl_service),
):
    target = await user_service.get_user_by_id(user_id)

    await acl_service.require_permission(
        user=current_user,
        element_code=BusinessElementEnum.USERS,
        action="read",
        owner_id=target.id,
    )

    return target


@router.patch("/me", response_model=UserBase)
async def update_me(
        payload: UserUpdateRequest,
        current_user: User = Depends(get_current_active_user),
        user_service: UserService = Depends(get_user_service),
):
    user = await user_service.update_me(current_user, payload)
    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
        current_user: User = Depends(get_current_active_user),
        user_service: UserService = Depends(get_user_service),
):
    """
    Мягкое удаление аккаунта:
    - is_active = False
    """
    await user_service.soft_delete_me(current_user)
    return None


@router.get("/", response_model=list[UserBase])
async def list_users(
        current_user: User = Depends(get_current_active_user),
        user_service: UserService = Depends(get_user_service),
        acl_service: ACLService = Depends(get_acl_service),
):
    await acl_service.require_permission(
        user=current_user,
        element_code=BusinessElementEnum.USERS,
        action="read",
        owner_id=None,
    )

    return await user_service.list_users()
