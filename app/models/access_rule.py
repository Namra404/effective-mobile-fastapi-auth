from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class AccessRoleRule(Base):

    __tablename__ = "access_roles_rules"

    id = Column(Integer, primary_key=True, index=True)

    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    element = Column(String(100), nullable=False, index=True)

    read_permission = Column(Boolean, default=False, nullable=False)
    create_permission = Column(Boolean, default=False, nullable=False)
    update_permission = Column(Boolean, default=False, nullable=False)
    delete_permission = Column(Boolean, default=False, nullable=False)

    read_all_permission = Column(Boolean, default=False, nullable=False)
    update_all_permission = Column(Boolean, default=False, nullable=False)
    delete_all_permission = Column(Boolean, default=False, nullable=False)

    role = relationship("Role", back_populates="access_rules")
