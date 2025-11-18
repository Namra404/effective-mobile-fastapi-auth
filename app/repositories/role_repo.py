from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role


class RoleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, role_id: int) -> Role | None:
        stmt = select(Role).where(Role.id == role_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Role | None:
        stmt = select(Role).where(Role.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Role]:
        stmt = select(Role)
        result = await self.session.scalars(stmt)
        return result.all()

    async def create(self, name: str) -> Role:
        role = Role(name=name)
        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)
        return role
