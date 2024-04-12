"""
Module of parking spots' CRUD
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, UUID, func
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
        user (User):
        session (AsyncSession): An asynchronous database session.

    Returns:
        ParkingSpot: The created parking spot object.
    """
    parking_spot = ParkingSpot(**body.model_dump(), user_id=user.id)
    session.add(parking_spot)
    await session.commit()
    return parking_spot


async def get_parking_spot_by_id(
    db: AsyncSession, parking_spot_id: int
) -> Optional[ParkingSpotDB]:
    """
    Retrieve a parking spot by its ID.

    Args:
        db (AsyncSession): An asynchronous database session.
        parking_spot_id (int): The ID of the parking spot to retrieve.

    Returns:
        Optional[ParkingSpotDB]: The parking spot, if found, otherwise None.
    """
    async with db() as session:
        stmt = select(ParkingSpotDB).filter(ParkingSpotDB.id == parking_spot_id)
        parking_spot = await session.execute(stmt)
        return parking_spot.scalar()


async def update_parking_spot(
    db: AsyncSession, parking_spot_id: int, new_parking_spot: ParkingSpotUpdate
) -> Optional[ParkingSpotDB]:
    """
    Update an existing parking spot in the database.

    Args:
        db (AsyncSession): An asynchronous database session.
        parking_spot_id (int): The ID of the parking spot to update.
        new_parking_spot (ParkingSpotUpdate): The updated parking spot information.

    Returns:
        Optional[ParkingSpotDB]: The updated parking spot object, if found, otherwise None.
    """
    async with db() as session:
        parking_spot = await get_parking_spot_by_id(parking_spot_id)
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
    db: AsyncSession, parking_spot_id: int, available: bool
) -> Optional[ParkingSpotDB]:
    """
    Update the availability status of a parking spot in the database.

    Args:
        db (AsyncSession): An asynchronous database session.
        parking_spot_id (int): The ID of the parking spot to update.
        available (bool): The new availability status of the parking spot.

    Returns:
        Optional[ParkingSpotDB]: The updated parking spot object, if found, otherwise None.
    """
    async with db() as session:
        parking_spot = await get_parking_spot_by_id(parking_spot_id)
        if parking_spot:
            parking_spot.is_available = available
            await session.commit()
            await session.refresh(parking_spot)
            return parking_spot
    return None


async def delete_parking_spot(db: AsyncSession, parking_spot_id: int) -> bool:
    """
    Delete a parking spot from the database.

    Args:
        db (AsyncSession): An asynchronous database session.
        parking_spot_id (int): The ID of the parking spot to delete.

    Returns:
        bool: True if the parking spot was successfully deleted, False otherwise.
    """
    async with db() as session:
        parking_spot = await get_parking_spot_by_id(parking_spot_id)
        if parking_spot:
            session.delete(parking_spot)
            await session.commit()
            return True
    return False


async def get_all_parking_spots(db: AsyncSession) -> List[ParkingSpotDB]:
    """
    Retrieve all parking spots from the database.

    Args:
        db (AsyncSession): An asynchronous database session.

    Returns:
        List[ParkingSpotDB]: A list of all parking spot objects.
    """
    async with db() as session:
        stmt = select(ParkingSpotDB)
        parking_spots = session.execute(stmt)
        return await parking_spots.scalars()
