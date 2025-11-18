from pydantic import BaseModel


class AccessRoleRuleBase(BaseModel):
    role_id: int
    element: str       
    read_permission: bool = False
    read_all_permission: bool = False
    create_permission: bool = False
    update_permission: bool = False
    update_all_permission: bool = False
    delete_permission: bool = False
    delete_all_permission: bool = False


class AccessRoleRuleUpdate(BaseModel):
    read_permission: bool | None = None
    read_all_permission: bool | None = None
    create_permission: bool | None = None
    update_permission: bool | None = None
    update_all_permission: bool | None = None
    delete_permission: bool | None = None
    delete_all_permission: bool | None = None


class AccessRoleRuleResponse(AccessRoleRuleBase):
    id: int


class AccessRoleRuleCreate(AccessRoleRuleBase):
    ...