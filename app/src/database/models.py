"""
Module with declaring of SQLAlchemy models
"""

from datetime import datetime, date
import enum
from typing import List

from sqlalchemy import (
    UUID,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Date,
    Boolean,
    Enum,
    CheckConstraint,
    Table,
    Column,
    func,
    text,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

from src.conf.config import settings


Base = declarative_base()


class IdAbstract(Base):
    __abstract__ = True
    id: Mapped[UUID | int] = (
        mapped_column(Integer, primary_key=True)
        if settings.test
        else mapped_column(
            UUID(as_uuid=True), primary_key=True, default=text("gen_random_uuid()")
        )
    )


class CreatedAtUpdatedAtAbstract(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class Role(enum.Enum):
    administrator: str = "administrator"
    user: str = "user"


class User(IdAbstract, CreatedAtUpdatedAtAbstract):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}
    username: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str] = mapped_column(String(254), nullable=True)
    last_name: Mapped[str] = mapped_column(String(254), nullable=True)
    phone: Mapped[str] = mapped_column(String(38), nullable=True)
    birthday: Mapped[date] = mapped_column(Date(), nullable=True)
    avatar: Mapped[str] = mapped_column(String(254), nullable=True)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.user)
    is_email_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_password_valid: Mapped[bool] = mapped_column(Boolean, default=True)
    cars: Mapped[List["Car"]] = relationship("Car", back_populates="user")

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @hybrid_property
    def is_active(self):
        return self.is_email_confirmed or self.is_password_valid


class Car(IdAbstract, CreatedAtUpdatedAtAbstract):
    __tablename__ = "cars"
    __mapper_args__ = {"eager_defaults": True}
    model: Mapped[str] = mapped_column(String(128), nullable=True)
    color: Mapped[str] = mapped_column(String(32), nullable=True)
    plate: Mapped[str] = mapped_column(String(32), nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    user_id: Mapped[UUID | int] = (
        mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
        if settings.test
        else mapped_column(
            UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
        )
    )
    user: Mapped["User"] = relationship("User", back_populates="cars")
