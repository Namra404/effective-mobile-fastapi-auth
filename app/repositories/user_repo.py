from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = (
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        stmt = (
            select(User)
            .options(selectinload(User.role))
            .where(User.email == email)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
            self,
            *,
            email: str,
            hashed_password: str,
            first_name: str | None = None,
            last_name: str | None = None,
            patronymic: str | None = None,
            role_id: int | None = None,
    ) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            role_id=role_id,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        stmt = (
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update(self, user: User, data: dict) -> User:
        for field, value in data.items():
            setattr(user, field, value)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def soft_delete(self, user: User) -> User:
        user.is_active = False
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def list_all(self) -> list[User]:
        stmt = select(User).options(selectinload(User.role))
        result = await self.session.scalars(stmt)
        return result.all()
