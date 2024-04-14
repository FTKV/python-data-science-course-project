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

from src.database.connect_db import get_session, get_redis_db1
from src.database.models import User, Role
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


@router.put(
    "",
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
    if car:
        car = await repository_cars.update_car(car_id, body, session)
    return car


@router.patch(
    "",
    response_model=CarResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def block_or_unblock_car(
    car_id: UUID4 | int,
    body: CarPatchModel,
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
    if car:
        car = await repository_cars.block_or_unblock_car(
            car_id, body.is_to_block, session
        )
    return car
