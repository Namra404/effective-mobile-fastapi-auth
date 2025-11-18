import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import hash_password
from app.core.enums import BusinessElementEnum
from app.db.databse import async_session_maker
from app.repositories.access_rule_repo import AccessRoleRuleRepository
from app.repositories.role_repo import RoleRepository
from app.repositories.user_repo import UserRepository
from app.schemas.acl import AccessRoleRuleCreate


async def seed_initial_data():
    async with async_session_maker() as session:
        role_repo = RoleRepository(session)
        user_repo = UserRepository(session)
        acl_repo = AccessRoleRuleRepository(session)

        admin_role = await role_repo.get_by_name("admin")
        if not admin_role:
            admin_role = await role_repo.create("admin")

        user_role = await role_repo.get_by_name("user")
        if not user_role:
            user_role = await role_repo.create("user")

        admin_email = "admin@example.com"
        admin = await user_repo.get_by_email(admin_email)
        if not admin:
            hashed = hash_password("admin").decode()
            admin = await user_repo.create(
                email=admin_email,
                hashed_password=hashed,
                first_name="Admin",
                last_name="User",
                patronymic=None,
                role_id=admin_role.id,
            )
            print(f"Создан admin: {admin_email}")
        else:
            # гарантируем, что у него роль admin
            if admin.role_id != admin_role.id:
                admin.role_id = admin_role.id
                session.add(admin)
                await session.commit()
                print(f"Пользователь {admin_email} назначен admin")

        existing_users_rules = await acl_repo.list_by_role_and_element(
            role_id=admin_role.id,
            element=BusinessElementEnum.USERS.value,
        )
        if not existing_users_rules:
            rule = AccessRoleRuleCreate(
                role_id=admin_role.id,
                element=BusinessElementEnum.USERS.value,
                read_permission=True,
                read_all_permission=True,
                create_permission=True,
                update_permission=True,
                update_all_permission=True,
                delete_permission=True,
                delete_all_permission=True,
            )
            await acl_repo.create(rule)
            print("Созданы ACL-правила для admin на USERS")

        existing_acl_rules = await acl_repo.list_by_role_and_element(
            role_id=admin_role.id,
            element=BusinessElementEnum.ACCESS_RULES.value,
        )
        if not existing_acl_rules:
            rule = AccessRoleRuleCreate(
                role_id=admin_role.id,
                element=BusinessElementEnum.ACCESS_RULES.value,
                read_permission=True,
                read_all_permission=True,
                create_permission=True,
                update_permission=True,
                update_all_permission=True,
                delete_permission=True,
                delete_all_permission=True,
            )
            await acl_repo.create(rule)
            print("Созданы ACL-правила для admin на ACCESS_RULES")

        existing_user_role_users_acl = await acl_repo.list_by_role_and_element(
            role_id=user_role.id,
            element=BusinessElementEnum.USERS.value,
        )
        if not existing_user_role_users_acl:
            rule = AccessRoleRuleCreate(
                role_id=user_role.id,
                element=BusinessElementEnum.USERS.value,

                read_permission=True,
                read_all_permission=False,
                create_permission=False,
                update_permission=True,
                update_all_permission=False,
                delete_permission=False,
                delete_all_permission=False,
            )
            await acl_repo.create(rule)
            print("Созданы ACL-правила для role=user на USERS")

        print("Seed completed")


if __name__ == "__main__":
    asyncio.run(seed_initial_data())
