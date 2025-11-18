from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import BusinessElementEnum
from app.db.databse import get_db_session
from app.models.user import User
from app.repositories.access_rule_repo import AccessRoleRuleRepository
from app.routes.dependencies import get_current_active_user, get_acl_service
from app.schemas.acl import (
    AccessRoleRuleCreate,
    AccessRoleRuleUpdate,
    AccessRoleRuleResponse,
)
from app.services.acl_service import ACLService

router = APIRouter(
    prefix="/api/v1/admin/acl",
    tags=["admin-acl"],
)


@router.get("/rules", response_model=list[AccessRoleRuleResponse])
async def list_access_rules(
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_db_session),
        acl_service: ACLService = Depends(get_acl_service),
):
    await acl_service.require_permission(
        user=current_user,
        element_code=BusinessElementEnum.ACCESS_RULES,
        action="read",
        owner_id=None,
    )

    repo = AccessRoleRuleRepository(session)
    rules = await repo.list_all()
    return rules


@router.post(
    "/rules",
    response_model=AccessRoleRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_access_rule(
        payload: AccessRoleRuleCreate,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_db_session),
        acl_service: ACLService = Depends(get_acl_service),
):
    await acl_service.require_permission(
        user=current_user,
        element_code=BusinessElementEnum.ACCESS_RULES,
        action="create",
        owner_id=None,
    )

    repo = AccessRoleRuleRepository(session)
    rule = await repo.create(payload)
    return rule


@router.patch("/rules/{rule_id}", response_model=AccessRoleRuleResponse)
async def update_access_rule(
        rule_id: int,
        payload: AccessRoleRuleUpdate,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_db_session),
        acl_service: ACLService = Depends(get_acl_service),
):
    await acl_service.require_permission(
        user=current_user,
        element_code=BusinessElementEnum.ACCESS_RULES,
        action="update",
        owner_id=None,
    )

    repo = AccessRoleRuleRepository(session)
    rule = await repo.get_by_id(rule_id)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found",
        )

    updated = await repo.update(rule, payload)
    return updated
