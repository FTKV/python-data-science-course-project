"""
Module of parking_spot' CRUD
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, UUID, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.database.models import User, ParkingSpot
from src.schemas.parking_spots import ParkingSpotModel, ParkingSpotDB, ParkingSpotUpdate


async def create_parking_spot(
    body: ParkingSpotModel, user: User, session: AsyncSession
) -> ParkingSpot:
    """
    Create a new parking spot in the database.

    Args:
        body (ParkingSpotModel): The parking spot object to be created.
        user (User): The user
        session (AsyncSession): An asynchronous database session.

    Returns:
        ParkingSpot: The created parking spot object.
    """
    parking_spot = ParkingSpot(**body.model_dump(), user_id=user.id)
    session.add(parking_spot)
    await session.commit()
    return parking_spot


async def get_parking_spot_by_id(
    parking_spot_id: UUID | int, session: AsyncSession
) -> ParkingSpot | None:
    """
    Retrieve a parking spot by its ID.

    Args:
        parking_spot_id (UUID | int): The ID of the parking spot to retrieve.
        session (AsyncSession): An asynchronous database session.

    Returns:
        ParkingSpot | None: The parking spot, if found, otherwise None.
    """
    stmt = select(ParkingSpot).filter(ParkingSpot.id == parking_spot_id)
    parking_spot = await session.execute(stmt)
    return parking_spot.scalar()


async def update_parking_spot(
    session: AsyncSession,
    parking_spot_id: UUID | int,
    new_parking_spot: ParkingSpotUpdate,
) -> ParkingSpot:
    """
    Update a parking spot in the database.

    Args:
        session (AsyncSession): An asynchronous database session.
        parking_spot_id (int): The ID of the parking spot to update.
        new_parking_spot (ParkingSpotUpdate): The updated parking spot information.

    Returns:
        Union[ParkingSpot, None]: The updated parking spot object, if found, otherwise None.
    """
    parking_spot = await get_parking_spot_by_id(parking_spot_id, session)
    if parking_spot:
        parking_spot.title = new_parking_spot.title
        parking_spot.description = new_parking_spot.description
        parking_spot.is_available = new_parking_spot.is_available
        parking_spot.is_out_of_service = new_parking_spot.is_out_of_service
        await session.commit()
        await session.refresh(parking_spot)
        return parking_spot
    return None


async def update_parking_spot_available_status(
    parking_spot_id: UUID | int, available: bool, session: AsyncSession
) -> ParkingSpot | None:
    """
    Update the availability status of a parking spot in the database.

    Args:
        parking_spot_id (UUID | int): The ID of the parking spot to update.
        available (bool): The new availability status of the parking spot.
        session (AsyncSession): An asynchronous database session.

    Returns:
        ParkingSpot | None: The updated parking spot object, if found, otherwise None.
    """
    parking_spot = await get_parking_spot_by_id(parking_spot_id, session)
    if parking_spot:
        parking_spot.is_available = available
        await session.commit()
        await session.refresh(parking_spot)
        return parking_spot
    return None


async def update_parking_spot_service_status(
    session: AsyncSession, parking_spot_id: UUID | int, out_of_service: bool
) -> ParkingSpot:
    """
    Update the service status of a parking spot.

    This function updates the service status (in-service or out-of-service) of a parking spot
    in the database. It takes the parking spot ID and the new service status as input.

    Args:
        session (AsyncSession): An asynchronous database session.
        parking_spot_id (int): The ID of the parking spot to update.
        out_of_service (bool): The new service status of the parking spot.

    Returns:
        ParkingSpot: The updated parking spot object, if found, otherwise None.
    """
    parking_spot = await get_parking_spot_by_id(parking_spot_id, session)
    if parking_spot:
        parking_spot.is_out_of_service = out_of_service
        await session.commit()
        await session.refresh(parking_spot)
        return parking_spot
    return None


async def delete_parking_spot(
    session: AsyncSession, parking_spot_id: UUID | int
) -> bool:
    """
    Delete a parking spot from the database.

    Args:
        session (AsyncSession): An asynchronous database session.
        parking_spot_id (int): The ID of the parking spot to delete.

    Returns:
        bool: True if the parking spot was successfully deleted, False otherwise.
    """
    parking_spot = await get_parking_spot_by_id(parking_spot_id, session)
    if parking_spot:
        session.delete(parking_spot)
        await session.commit()
        return True
    return False


async def get_all_parking_spots(session: AsyncSession) -> List[ParkingSpot]:
    """
    Retrieve all parking spots from the database.

    Args:
        db (AsyncSession): An asynchronous database session.

    Returns:
        List[ParkingSpotDB]: A list of all parking spot objects.
    """
    stmt = select(ParkingSpot)
    parking_spots = session.execute(stmt)
    return await parking_spots


async def get_all_occupied_parking_spots(session: AsyncSession) -> List[ParkingSpot]:
    stmt = select(ParkingSpot).filter(
        and_(ParkingSpot.is_available == False, ParkingSpot.is_out_of_service == False)
    )
    parking_spots = await session.execute(stmt)
    return parking_spots.scalars()


async def get_random_available_parking_spot(session: AsyncSession) -> ParkingSpot:
    """
    Retrieve a random available parking spot from the database.

    This function retrieves a random available parking spot from the database.
    It filters parking spots based on availability (is_available == True) and service status
    (is_out_of_service == False), and then selects one randomly.

    Args:
        session (AsyncSession): An asynchronous database session.

    Returns:
        ParkingSpot: A random available parking spot object, if found.
    """
    stmt = (
        select(ParkingSpot)
        .filter(
            and_(
                ParkingSpot.is_available == True, ParkingSpot.is_out_of_service == False
            )
        )
        .order_by(func.random())
    )
    parking_spot = await session.execute(stmt)
    return parking_spot.scalar()
