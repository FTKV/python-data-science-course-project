"""
Module of cars' CRUD
"""

from sqlalchemy import select, UUID
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import settings
from src.database.models import User, Car
from src.schemas.cars import CarRecognizedPlateModel, CarUpdateModel
from src.services.cloudinary import cloudinary_service


async def create_car(body: CarRecognizedPlateModel, session: AsyncSession) -> Car:
    """
    Creates a new car.

    :param body: The body for the car to create.
    :type body: FinancialTransactionModel
    :param session: The database session.
    :type session: AsyncSession
    :return: The newly created car.
    :rtype: Car
    """
    car = Car(**body.model_dump())
    session.add(car)
    await session.commit()
    await session.refresh(car)
    return car


async def read_cars(offset: int, limit: int, session: AsyncSession) -> ScalarResult:
    """
    Gets all cars.

    :param offset: The number of cars to skip.
    :type offset: int
    :param limit: The maximum number of cars to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The ScalarResult with the list of cars.
    :rtype: ScalarResult
    """
    stmt = select(Car)
    stmt = stmt.offset(offset).limit(limit)
    cars = await session.execute(stmt)
    return cars.scalars()


async def read_cars_by_user_id(
    user_id: UUID | int, offset: int, limit: int, session: AsyncSession
) -> ScalarResult:
    """
    Gets cars by user with the specified id.

    :param user_id: The ID of the user to get cars.
    :type user_id: UUID | int
    :param offset: The number of cars to skip.
    :type offset: int
    :param limit: The maximum number of cars to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The ScalarResult with the list of cars.
    :rtype: ScalarResult
    """
    stmt = select(Car).filter(Car.user_id == user_id)
    stmt = stmt.offset(offset).limit(limit)
    cars = await session.execute(stmt)
    return cars.scalars()


async def read_car_by_car_id(
    car_id: UUID | int,
    session: AsyncSession,
) -> Car | None:
    """
    Gets a car with the specified id.

    :param car_id: The ID of the car to get.
    :type car_id: UUID | int
    :param session: The database session.
    :type session: AsyncSession
    :return: The car with the specified ID, or None if it does not exist.
    :rtype: Car | None
    """
    stmt = select(Car).filter(Car.id == car_id)
    car = await session.execute(stmt)
    return car.scalar()


async def read_car_by_plate(
    plate: str,
    session: AsyncSession,
) -> Car | None:
    """
    Gets a car with the specified plate.

    :param plate: The plate of the car to get.
    :type plate: str
    :param session: The database session.
    :type session: AsyncSession
    :return: The car with the specified plate, or None if it does not exist.
    :rtype: Car | None
    """
    stmt = select(Car).filter(Car.plate == plate)
    car = await session.execute(stmt)
    return car.scalar()


async def update_car(
    car_id: UUID | int, body: CarUpdateModel, session: AsyncSession
) -> Car | None:
    """
    Updates a car with the specified id.

    :param car_id: The ID of the car to update.
    :type car_id: UUID | int
    :param body: The data for the car to update.
    :type body: CarUpdateModel
    :param session: The database session.
    :type session: AsyncSession
    :return: The car with the specified ID, or None if it does not exist.
    :rtype: Car | None
    """
    stmt = select(Car).filter(Car.id == car_id)
    car = await session.execute(stmt)
    car = car.scalar()
    if car:
        if body.model:
            car.model = body.model
        if body.color:
            car.color = body.color
        if body.description:
            car.description = body.description
        if body.user_id:
            car.user_id = body.user_id
        await session.commit()
    return car


async def block_or_unblock_car(
    car_id: UUID | int, is_to_block: bool, session: AsyncSession
) -> Car | None:
    """
    Blocks or unblocks a car with the specified id.

    :param car_id: The ID of the car to blocks or unblock.
    :type car_id: UUID | int
    :param is_to_block: The value to block or unblock the car.
    :type is_to_block: bool
    :param session: The database session.
    :type session: AsyncSession
    :return: The car with the specified ID, or None if it does not exist.
    :rtype: Car | None
    """
    stmt = select(Car).filter(Car.id == car_id)
    car = await session.execute(stmt)
    car = car.scalar()
    if car:
        car.is_blacklisted = is_to_block
        await session.commit()
    return car
