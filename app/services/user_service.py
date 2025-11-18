from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.routes.mapper import user_to_schema
from app.schemas.users import UserUpdateRequest, UserBase


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def get_me(self, current_user: User) -> UserBase:
        return user_to_schema(current_user)

    async def update_me(
            self,
            current_user: User,
            payload: UserUpdateRequest,
    ) -> UserBase:
        data = payload.model_dump(exclude_unset=True)
        if not data:
            return user_to_schema(current_user)

        updated = await self.user_repo.update(current_user, data)
        return user_to_schema(updated)

    async def soft_delete_me(self, current_user: User) -> User:
        if not current_user.is_active:
            return current_user
        return await self.user_repo.soft_delete(current_user)

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def list_users(self) -> list[UserBase]:
        users = await self.user_repo.list_all()
        return [user_to_schema(user) for user in users]