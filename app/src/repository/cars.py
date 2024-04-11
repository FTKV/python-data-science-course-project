"""
Module of cars' CRUD
"""

from sqlalchemy import select, UUID
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import settings
from src.database.models import User, Car
from src.schemas.cars import CarModel, CarUpdateModel
from src.services.cloudinary import cloudinary_service


async def create_car(data: CarModel, session: AsyncSession) -> Car:
    # TODO recognizing picture into text
    car = Car(**data.model_dump())
    session.add(car)
    await session.commit()
    await session.refresh(car)
    return car


async def read_cars(session: AsyncSession) -> ScalarResult:
    """
    Gets all cars.

    :param session: The database session.
    :type session: AsyncSession
    :return: The ScalarResult with the list of cars.
    :rtype: ScalarResult
    """
    stmt = select(Car)
    cars = await session.execute(stmt)
    return cars.scalars()


async def read_cars_by_user_id(
    user_id: UUID | int, session: AsyncSession
) -> ScalarResult:
    """
    Gets cars by user with the specified id.

    :param user_id: The ID of the user to get cars.
    :type user_id: UUID | int
    :param session: The database session.
    :type session: AsyncSession
    :return: The ScalarResult with the list of cars.
    :rtype: ScalarResult
    """
    stmt = select(Car).filter(Car.user_id == user_id)
    cars = await session.execute(stmt)
    return cars.scalars()


async def read_car(
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
        await session.commit()
    return car


async def blacklist_car(car_id: UUID | int, session: AsyncSession) -> Car | None:
    """
    Blacklists a car with the specified id.

    :param car_id: The ID of the car to blacklist.
    :type car_id: UUID | int
    :param session: The database session.
    :type session: AsyncSession
    :return: The car with the specified ID, or None if it does not exist.
    :rtype: Car | None
    """
    stmt = select(Car).filter(Car.id == car_id)
    car = await session.execute(stmt)
    car = car.scalar()
    if car:
        car.is_blacklisted = True
        await session.commit()
    return car
