"""
Module of cars' routes
"""

from typing import List

from pydantic import UUID4
from fastapi import APIRouter, HTTPException, Depends, Form, status, Query
from fastapi.responses import FileResponse
from redis.asyncio.client import Redis
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import REPORTS_DIR
from src.database.connect_db import get_session, get_redis_db1
from src.database.models import User, Role
from src.reports import reservations as reports_reservations
from src.repository import cars as repository_cars
from src.schemas.cars import (
    CarUnrecognizedPlateModel,
    CarRecognizedPlateModel,
    CarUpdateModel,
    CarPatchModel,
    CarResponse,
)
from src.services.ai_models import process_image
from src.services.auth import auth_service
from src.services.roles import RoleAccess


router = APIRouter(prefix="/cars", tags=["cars"])

allowed_operations_for_self = RoleAccess([Role.administrator, Role.user])
allowed_operations_for_all = RoleAccess([Role.administrator])


@router.post(
    "/unrecognized",
    response_model=CarResponse,
    dependencies=[Depends(allowed_operations_for_self)],
)
async def read_or_create_car_with_unrecognized_plate(
    data: CarUnrecognizedPlateModel = Depends(CarUnrecognizedPlateModel.as_form),
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a POST-operation to "/unrecognized" car subroute and reads or creates a car.

    :param data: The data for the car to read or create.
    :type data: CarUnrecognizedPlateModel
    :param session: Get the database session
    :type AsyncSession: The current session.
    :return: Read of newly created car.
    :rtype: Car
    """
    data.plate = await process_image(data.plate.file)
    try:
        data = CarRecognizedPlateModel(**data.model_dump())
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found or license plate was recognized incorrectly",
        )
    car = await repository_cars.read_car_by_plate(data.plate, session)
    if not car:
        car = await repository_cars.create_car(data, session)
    return car


@router.post(
    "/recognized",
    response_model=CarResponse,
    dependencies=[Depends(allowed_operations_for_self)],
)
async def read_or_create_car_with_recognized_plate(
    body: CarRecognizedPlateModel = Depends(CarRecognizedPlateModel.as_form),
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a POST-operation to "/recognized" car subroute and reads or creates a car.

    :param data: The data for the car to read or create.
    :type data: CarRecognizedPlateModel
    :param session: Get the database session
    :type AsyncSession: The current session.
    :return: Read of newly created car.
    :rtype: Car
    """
    car = await repository_cars.read_car_by_plate(body.plate, session)
    if not car:
        car = await repository_cars.create_car(body, session)
    return car


@router.get(
    "",
    response_model=List[CarResponse],
    dependencies=[Depends(allowed_operations_for_all)],
)
async def read_cars(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> ScalarResult:
    """
    Handles a GET-operation to cars route and gets all cars.

    :param offset: The number of cars to skip.
    :type offset: int
    :param limit: The maximum number of cars to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The ScalarResult with the list of cars.
    :rtype: ScalarResult
    """
    cars = await repository_cars.read_cars(offset, limit, session)
    return cars


@router.put(
    "/{car_id}",
    response_model=CarResponse,
    dependencies=[Depends(allowed_operations_for_self)],
)
async def update_car(
    car_id: UUID4 | int,
    body: CarUpdateModel = Depends(CarUpdateModel.as_form),
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a PUT-operation to "" car subroute and updates a car.

    :param car_id: The car id.
    :type car_id: UUID4 | int
    :param body: The data for the car to update.
    :type body: CarUpdateModel
    :param session: Get the database session
    :type AsyncSession: The current session.
    :return: The updated car.
    :rtype: Car
    """
    car = await repository_cars.read_car_by_car_id(car_id, session)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found",
        )
    car = await repository_cars.update_car(car_id, body, session)
    return car


@router.patch(
    "/{car_id}",
    response_model=CarResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def block_or_unblock_car(
    car_id: UUID4 | int,
    body: CarPatchModel = Depends(CarPatchModel.as_form),
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a PATCH-operation to "" car subroute and blocks or unblocks a car.

    :param car_id: The car id.
    :type car_id: UUID4 | int
    :param body: The data for the car to patch.
    :type body: CarPatchModel
    :param session: Get the database session
    :type AsyncSession: The current session.
    :return: The blocked or unblocked car.
    :rtype: Car
    """
    car = await repository_cars.read_car_by_car_id(car_id, session)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found",
        )
    car = await repository_cars.block_or_unblock_car(car_id, body.is_to_block, session)
    return car


@router.get(
    "/{car_id}/reservations",
    response_class=FileResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def get_car_checked_out_reservations(
    car_id: UUID4 | int,
    session: AsyncSession = Depends(get_session),
):
    return await reports_reservations.get_car_checked_out_reservations(car_id, session)
    # return FileResponse(
    #     REPORTS_DIR,
    #     media_type="text/csv",
    #     filename="report.csv",
    #     status_code=200,
    # )
