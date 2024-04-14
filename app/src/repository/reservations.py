"""
Module of reservation' CRUD
"""

from typing import Union
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Reservation
from src.schemas.reservations import ReservationModel, ReservationUpdateModel


async def create_reservation(reservation_data: ReservationModel, session: AsyncSession):
    """
    Create a new reservation in the database.

    Args:
        session (AsyncSession): An asynchronous database session.
        reservation_data (ReservationModel): The data of the reservation to create.

    Returns:
        Reservation: The created reservation object.
    """
    reservation = Reservation(**reservation_data.model_dump())
    session.add(reservation)
    await session.commit()
    await session.refresh(reservation)
    return reservation


async def get_reservation_by_id(reservation_id: UUID | int, session: AsyncSession):
    """
    Retrieve a reservation by its ID from the database.

    Args:
        session (AsyncSession): An asynchronous database session.
        reservation_id (int): The ID of the reservation to retrieve.

    Returns:
        Reservation: The retrieved reservation object, if found, otherwise None.
    """
    query = select(Reservation).filter(Reservation.id == reservation_id)
    result = await session.execute(query)
    return result.scalar()


async def get_reservations_by_user_id(
    user_id: UUID | int, offset: int, limit: int, session: AsyncSession
):
    """
    Retrieve all reservations associated with a specific user from the database.

    Args:
        session (AsyncSession): An asynchronous database session.
        user_id (Union[UUID4, int]): The ID of the user.

    Returns:
        List[Reservation]: A list of reservations associated with the user.
    """
    stmt = select(Reservation).filter(Reservation.user_id == user_id)
    stmt = stmt.offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars()


async def get_all_reservations(offset: int, limit: int, session: AsyncSession):
    """
    Retrieve all reservations from the database.

    Args:
        session (AsyncSession): An asynchronous database session.

    Returns:
        List[Reservation]: A list of all reservations in the database.
    """
    stmt = select(Reservation)
    stmt = stmt.offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars()


async def update_reservation(
    reservation_id: UUID | int,
    reservation_data: ReservationUpdateModel,
    session: AsyncSession,
) -> Reservation | None:
    """
    Update a reservation in the database.

    Args:
        session (AsyncSession): An asynchronous database session.
        reservation_id (int): The ID of the reservation to update.
        reservation_data (ReservationUpdateModel): The updated reservation information.

    Returns:
        Union[Reservation, None]: The updated reservation object, if found, otherwise None.
    """
    reservation = await get_reservation_by_id(reservation_id, session)
    if reservation:
        for key, value in reservation_data.model_dump().items():
            if hasattr(reservation, key):
                setattr(reservation, key, value)
        await session.commit()
        await session.refresh(reservation)
        return reservation
    return None
