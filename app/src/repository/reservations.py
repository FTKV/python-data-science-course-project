"""
Module for performing CRUD operations on reservations.
"""

from typing import Union
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.database.models import Reservation, FinancialTransaction
from src.schemas.reservations import ReservationModel, ReservationUpdateModel


async def create_reservation(reservation_data: ReservationModel, session: AsyncSession):
    """
    Create a new reservation in the database.

    Args:
        reservation_data (ReservationModel): The data of the reservation to create.
        session (AsyncSession): An asynchronous database session.

    Returns:
        Reservation: The created reservation object.
    """
    if reservation_data.user_id is None:
        return ValueError("User ID cannot be None")
    reservation = Reservation(**reservation_data.model_dump(), debit=0.00, credit=0.00)
    session.add(reservation)
    await session.commit()
    await session.refresh(reservation)
    return reservation



async def get_reservation_by_id(reservation_id: UUID4 | int, session: AsyncSession):
    """
    Retrieve a reservation by its ID from the database.

    Args:
        reservation_id (Union[UUID4, int]): The ID of the reservation to retrieve.
        session (AsyncSession): An asynchronous database session.

    Returns:
        Reservation: The retrieved reservation object, if found, otherwise None.
    """
    query = select(Reservation).filter(Reservation.id == reservation_id)
    result = await session.execute(query)
    return result.scalar()


async def get_reservations_by_user_id(
    user_id: UUID4 | int, offset: int, limit: int, session: AsyncSession
):
    """
    Retrieve all reservations associated with a specific user from the database.

    Args:
        user_id (Union[UUID4, int]): The ID of the user.
        offset (int): The offset for pagination.
        limit (int): The limit for pagination.
        session (AsyncSession): An asynchronous database session.

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
        offset (int): The offset for pagination.
        limit (int): The limit for pagination.
        session (AsyncSession): An asynchronous database session.

    Returns:
        List[Reservation]: A list of all reservations in the database.
    """
    stmt = select(Reservation)
    stmt = stmt.offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars()


async def update_reservation(
    reservation_id: UUID4 | int,
    reservation_data: ReservationUpdateModel,
    session: AsyncSession,
) -> Reservation | None:
    """
    Update a reservation in the database.

    Args:
        reservation_id (Union[UUID4, int]): The ID of the reservation to update.
        reservation_data (ReservationUpdateModel): The updated reservation information.
        session (AsyncSession): An asynchronous database session.

    Returns:
        Union[Reservation, None]: The updated reservation object, if found, otherwise None.
    """
    reservation = await get_reservation_by_id(reservation_id, session)
    if reservation:
        for key, value in reservation_data.model_dump().items():
            if hasattr(reservation, key) and value is not None:
                setattr(reservation, key, value)
        await session.commit()
        await session.refresh(reservation)
        return reservation
    return None


async def get_debit_credit_of_reservation(reservation_id, session):
    """
    Retrieve the total debit and credit amounts associated with a reservation.

    Args:
        reservation_id: The ID of the reservation to retrieve totals for.
        session: An asynchronous database session.

    Returns:
        Tuple[float, float]: A tuple containing the total debit and credit amounts.
            If no transactions are found for the reservation, (0.0, 0.0) is returned.
    """
    stmt = (
        select(
            func.sum(FinancialTransaction.debit), func.sum(FinancialTransaction.credit)
        )
        .select_from(FinancialTransaction)
        .filter(FinancialTransaction.reservation_id == reservation_id)
        .group_by(FinancialTransaction.reservation_id)
    )
    result = await session.execute(stmt)
    totals = result.all()
    return totals[0] if totals else (0.0, 0.0)
