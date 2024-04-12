"""
Module of reservation' CRUD
"""

from typing import Union
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Reservation
from src.schemas.reservations import ReservationModel, ReservationUpdateModel


async def create_reservation(session: AsyncSession, reservation_data: ReservationModel):
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
    return reservation

async def get_reservation_by_id(session: AsyncSession, reservation_id: int):
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
    return result.scalar_one_or_none()

async def get_reservations_by_user_id(session: AsyncSession, user_id: Union[UUID4, int]):
    """
    Retrieve all reservations associated with a specific user from the database.

    Args:
        session (AsyncSession): An asynchronous database session.
        user_id (Union[UUID4, int]): The ID of the user.

    Returns:
        List[Reservation]: A list of reservations associated with the user.
    """
    query = select(Reservation).filter(Reservation.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()

async def get_all_reservations(session: AsyncSession):
    """
    Retrieve all reservations from the database.

    Args:
        session (AsyncSession): An asynchronous database session.

    Returns:
        List[Reservation]: A list of all reservations in the database.
    """
    query = select(Reservation)
    result = await session.execute(query)
    return result.scalars().all()

async def update_reservation(
    session: AsyncSession, reservation_id: int, reservation_data: ReservationUpdateModel
) -> Union[Reservation, None]:
    """
    Update a reservation in the database.

    Args:
        session (AsyncSession): An asynchronous database session.
        reservation_id (int): The ID of the reservation to update.
        reservation_data (ReservationUpdateModel): The updated reservation information.

    Returns:
        Union[Reservation, None]: The updated reservation object, if found, otherwise None.
    """
    reservation = await get_reservation_by_id(session, reservation_id)
    if reservation:
        for key, value in reservation_data.model_dump().items():
            if hasattr(reservation, key):
                setattr(reservation, key, value)
        await session.commit()
        await session.refresh(reservation)
        return reservation
    return None
