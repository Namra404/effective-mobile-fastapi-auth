from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.access_rule import AccessRoleRule
from app.schemas.acl import AccessRoleRuleUpdate, AccessRoleRuleCreate


class AccessRoleRuleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_by_role_and_element(
            self,
            role_id: int,
            element: str,
    ) -> list[AccessRoleRule]:
        stmt = (
            select(AccessRoleRule)
            .where(
                AccessRoleRule.role_id == role_id,
                AccessRoleRule.element == element,
            )
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def list_all(self) -> list[AccessRoleRule]:
        stmt = select(AccessRoleRule)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_by_id(self, rule_id: int) -> AccessRoleRule | None:
        stmt = select(AccessRoleRule).where(AccessRoleRule.id == rule_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: AccessRoleRuleCreate) -> AccessRoleRule:
        rule = AccessRoleRule(**data.model_dump())
        self.session.add(rule)
        await self.session.commit()
        await self.session.refresh(rule)
        return rule

    async def update(
            self,
            rule: AccessRoleRule,
            data: AccessRoleRuleUpdate,
    ) -> AccessRoleRule:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(rule, field, value)
        self.session.add(rule)
        await self.session.commit()
        await self.session.refresh(rule)
        return rule
