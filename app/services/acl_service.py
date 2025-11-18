from fastapi import HTTPException, status

from app.core.enums import BusinessElementEnum
from app.models import User
from app.models.access_rule import AccessRoleRule
from app.repositories.access_rule_repo import AccessRoleRuleRepository


class ACLService:
    def __init__(self, access_repo: AccessRoleRuleRepository) -> None:
        self.access_repo = access_repo

    async def require_permission(
            self,
            user: User,
            element_code: str | BusinessElementEnum,
            action: str,
            owner_id: int | None = None,
    ) -> None:
        if isinstance(element_code, BusinessElementEnum):
            element_code = element_code.value

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
            )

        if not user.role_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No role assigned",
            )

        rules = await self.access_repo.list_by_role_and_element(
            role_id=user.role_id,
            element=element_code,
        )
        if not rules:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No rules for this",
            )

        allowed = False
        for rule in rules:
            if self._check_rule(rule, action, user_id=user.id, owner_id=owner_id):
                allowed = True
                break

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )

    @staticmethod
    def _check_rule(
            rule: AccessRoleRule,
            action: str,
            user_id: int,
            owner_id: int | None,
    ) -> bool:
        if action == "read":
            if rule.read_all_permission:
                return True
            if (
                    owner_id is not None
                    and rule.read_permission
                    and owner_id == user_id
            ):
                return True

        elif action == "create":
            if rule.create_permission:
                return True

        elif action == "update":
            if rule.update_all_permission:
                return True
            if (
                    owner_id is not None
                    and rule.update_permission
                    and owner_id == user_id
            ):
                return True

        elif action == "delete":
            if rule.delete_all_permission:
                return True
            if (
                    owner_id is not None
                    and rule.delete_permission
                    and owner_id == user_id
            ):
                return True

        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unknown action: {action}",
            )

        return False
