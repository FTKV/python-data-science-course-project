"""
Module with declaring of SQLAlchemy models
"""

from datetime import datetime, date, time
import enum
from typing import List

from sqlalchemy import (
    UUID,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Date,
    Time,
    Boolean,
    Enum,
    Numeric,
    CheckConstraint,
    Table,
    Column,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM
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
    role: Mapped[Enum] = mapped_column(ENUM(Role), default=Role.user)
    is_email_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_password_valid: Mapped[bool] = mapped_column(Boolean, default=True)
    cars: Mapped[List["Car"]] = relationship("Car", back_populates="user")
    rates: Mapped[List["Rate"]] = relationship("Rate", back_populates="user")
    rate_details: Mapped[List["RateDetail"]] = relationship(
        "RateDetail", back_populates="user"
    )
    parking_spots: Mapped[List["ParkingSpot"]] = relationship(
        "ParkingSpot", back_populates="user"
    )
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", back_populates="user"
    )
    financial_transactions: Mapped[List["FinancialTransaction"]] = relationship(
        "FinancialTransaction", back_populates="user"
    )

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @hybrid_property
    def is_active(self):
        return self.is_email_confirmed or self.is_password_valid


class Car(IdAbstract, CreatedAtUpdatedAtAbstract):
    __tablename__ = "cars"
    __mapper_args__ = {"eager_defaults": True}
    plate: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(128), nullable=True)
    color: Mapped[str] = mapped_column(String(32), nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    is_blacklisted: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[UUID | int] = (
        mapped_column(
            Integer,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
        )
        if settings.test
        else mapped_column(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
        )
    )
    user: Mapped["User"] = relationship("User", back_populates="cars")
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", back_populates="car"
    )


class Rate(IdAbstract, CreatedAtUpdatedAtAbstract):
    __tablename__ = "rates"
    __mapper_args__ = {"eager_defaults": True}
    title: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    is_daily: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[UUID | int] = (
        mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
        if settings.test
        else mapped_column(
            UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
        )
    )
    user: Mapped["User"] = relationship("User", back_populates="rates")
    rate_details: Mapped[List["RateDetail"]] = relationship(
        "RateDetail", back_populates="rate"
    )
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", back_populates="rate"
    )


class RateDetail(IdAbstract, CreatedAtUpdatedAtAbstract):
    __tablename__ = "rate_details"
    __mapper_args__ = {"eager_defaults": True}
    start_date: Mapped[date] = mapped_column(Date(), server_default=func.now())
    end_date: Mapped[date] = mapped_column(Date(), server_default=func.now())
    start_hour: Mapped[time] = mapped_column(Time(), default=time())
    end_hour: Mapped[time] = mapped_column(Time(), default=time())
    amount: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    user_id: Mapped[UUID | int] = (
        mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
        if settings.test
        else mapped_column(
            UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
        )
    )
    rate_id: Mapped[UUID | int] = (
        mapped_column(Integer, ForeignKey("rates.id", ondelete="CASCADE"))
        if settings.test
        else mapped_column(
            UUID(as_uuid=True), ForeignKey("rates.id", ondelete="CASCADE")
        )
    )
    user: Mapped["User"] = relationship("User", back_populates="rate_details")
    rate: Mapped["Rate"] = relationship("Rate", back_populates="rate_details")


class Status(enum.Enum):
    CHECKED_IN: str = "CHECKED_IN"
    CHECKED_OUT: str = "CHECKED_OUT"


class Event(IdAbstract):
    __tablename__ = "events"
    __mapper_args__ = {"eager_defaults": True}
    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    event_type: Mapped[Enum] = mapped_column(ENUM(Status))
    parking_spot_id: Mapped[UUID | int] = (
        mapped_column(Integer, ForeignKey("parking_spots.id", ondelete="SET NULL"))
        if settings.test
        else mapped_column(
            UUID(as_uuid=True), ForeignKey("parking_spots.id", ondelete="SET NULL")
        )
    )
    reservation_id: Mapped[UUID | int] = (
        mapped_column(
            Integer,
            ForeignKey("reservations.id", ondelete="SET NULL"),
            nullable=True,
        )
        if settings.test
        else mapped_column(
            UUID(as_uuid=True),
            ForeignKey("reservations.id", ondelete="SET NULL"),
            nullable=True,
        )
    )
    parking_spot: Mapped["ParkingSpot"] = relationship(
        "ParkingSpot", back_populates="events"
    )
    reservation: Mapped["Reservation"] = relationship(
        "Reservation", back_populates="events"
    )


class ParkingSpot(IdAbstract, CreatedAtUpdatedAtAbstract):
    __tablename__ = "parking_spots"
    __mapper_args__ = {"eager_defaults": True}
    title: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    is_out_of_service: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[UUID | int] = (
        mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
        if settings.test
        else mapped_column(
            UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
        )
    )
    user: Mapped["User"] = relationship("User", back_populates="parking_spots")
    events: Mapped[List["Event"]] = relationship("Event", back_populates="parking_spot")


class Reservation(IdAbstract, CreatedAtUpdatedAtAbstract):
    __tablename__ = "reservations"
    __mapper_args__ = {"eager_defaults": True}
    resv_status: Mapped[Enum] = mapped_column(ENUM(Status))
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    debit: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    credit: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    user_id: Mapped[UUID | int] = (
        mapped_column(
            Integer,
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        )
        if settings.test
        else mapped_column(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        )
    )
    parking_spot_id: Mapped[UUID | int] = (
        mapped_column(
            Integer,
            ForeignKey("parking_spots.id", ondelete="SET NULL"),
            nullable=True,
        )
        if settings.test
        else mapped_column(
            UUID(as_uuid=True),
            ForeignKey("parking_spots.id", ondelete="SET NULL"),
            nullable=True,
        )
    )
    car_id: Mapped[UUID | int] = (
        mapped_column(Integer, ForeignKey("cars.id", ondelete="SET NULL"))
        if settings.test
        else mapped_column(
            UUID(as_uuid=True), ForeignKey("cars.id", ondelete="SET NULL")
        )
    )
    rate_id: Mapped[UUID | int] = (
        mapped_column(Integer, ForeignKey("rates.id", ondelete="SET NULL"))
        if settings.test
        else mapped_column(
            UUID(as_uuid=True), ForeignKey("rates.id", ondelete="SET NULL")
        )
    )
    user: Mapped["User"] = relationship("User", back_populates="reservations")
    car: Mapped["Car"] = relationship("Car", back_populates="reservations")
    rate: Mapped["Rate"] = relationship("Rate", back_populates="reservations")
    events: Mapped[List["Event"]] = relationship("Event", back_populates="reservation")
    financial_transactions: Mapped[List["FinancialTransaction"]] = relationship(
        "FinancialTransaction", back_populates="reservation"
    )


class TrxType(enum.Enum):
    PAYMENT: str = "Payment"
    CHARGE: str = "Charge"


class FinancialTransaction(IdAbstract):
    __tablename__ = "financial_transactions"
    __mapper_args__ = {"eager_defaults": True}
    trx_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    trx_type: Mapped[Enum] = mapped_column(ENUM(TrxType))
    debit: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    credit: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    user_id: Mapped[UUID | int] = (
        mapped_column(
            Integer,
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        )
        if settings.test
        else mapped_column(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        )
    )
    reservation_id: Mapped[UUID | int] = (
        mapped_column(Integer, ForeignKey("reservations.id", ondelete="SET NULL"))
        if settings.test
        else mapped_column(
            UUID(as_uuid=True), ForeignKey("reservations.id", ondelete="SET NULL")
        )
    )
    user: Mapped["User"] = relationship("User", back_populates="financial_transactions")
    reservation: Mapped["Reservation"] = relationship(
        "Reservation", back_populates="financial_transactions"
    )
