from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Role(Base):

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    users = relationship("User", back_populates="role")

    access_rules = relationship(
        "AccessRoleRule",
        back_populates="role",
        cascade="all, delete-orphan",
    )
