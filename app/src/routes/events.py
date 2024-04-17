"""
Module of events' routes
"""

from pydantic import UUID4
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from redis.asyncio.client import Redis
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connect_db import get_session, get_redis_db1
from src.database.models import Event, Role, Status
from src.repository import cars as repository_cars
from src.repository import events as repository_events
from src.repository import parking_spots as repository_parking_spots
from src.repository import rates as repository_rates
from src.repository import reservations as repository_reservations
from src.services.ai_models import process_image
from src.services.auth import auth_service
from src.services.roles import RoleAccess
from src.schemas.cars import CarRecognizedPlateModel
from src.schemas.events import EventModel, EventImageModel, EventDB
from src.schemas.reservations import ReservationModel, ReservationUpdateModel

router = APIRouter(prefix="/events", tags=["events"])

allowed_operations_for_self = RoleAccess([Role.administrator, Role.user])
allowed_operations_for_all = RoleAccess([Role.administrator])


@router.post(
    "/{event_type}",
    response_model=EventDB,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def create_event(
    event_type: Status,
    data: EventImageModel = Depends(EventImageModel.as_form),
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a POST-operation to "{id}" event subroute and create an event.

    :param data: The data for the event to create.
    :type data: EventModel
    :type AsyncSession: The current session.
    :return: Newly created event.
    :rtype: Event
    """
    data.plate = await process_image(data.plate.file)
    try:
        data = CarRecognizedPlateModel(plate=data.plate)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found or license plate was recognized incorrectly",
        )
    car = await repository_cars.read_car_by_plate(data.plate, session)
    if event_type == Status.CHECKED_IN:
        if not car:
            car = await repository_cars.create_car(data, session)
        if await repository_cars.is_car_blocked(car.plate, session):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Car is blocked!",
            )
        parking_spot = await repository_parking_spots.get_random_available_parking_spot(
            session
        )
        if not parking_spot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No available parking spots",
            )
        rate = await repository_rates.get_default_rate(session)
        data = ReservationModel(
            resv_status=event_type,
            user_id=car.user_id,
            parking_spot_id=parking_spot.id,
            car_id=car.id,
            rate_id=rate.id,
        )
        reservation = await repository_reservations.create_reservation(data, session)
        await repository_parking_spots.update_parking_spot_available_status(
            reservation.parking_spot_id, False, session
        )
    elif event_type == Status.CHECKED_OUT:
        if not car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found or license plate was recognized incorrectly",
            )
        reservation = await repository_reservations.get_in_house_reservation_by_car_id(
            car.id, session
        )
        balance = reservation.debit - reservation.credit
        if balance > 0:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"Balance is not zero! Should be payment for {balance} UAH",
            )
        if balance < 0:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"Balance is not zero! Should be withdraw for {balance} UAH",
            )
        data = ReservationUpdateModel(
            resv_status=event_type,
            user_id=car.user_id,
        )
        reservation = await repository_reservations.update_reservation(
            reservation.id, data, session
        )
        await repository_parking_spots.update_parking_spot_available_status(
            reservation.parking_spot_id, True, session
        )
    data = EventModel(
        parking_spot_id=reservation.parking_spot_id, reservation_id=reservation.id
    )
    event = await repository_events.create_event(event_type, data, session)
    return event


@router.get(
    "/{event_id}",
    response_model=EventDB,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def read_event(
    event_id: UUID4 | int,
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a GET-operation to '/{id}' event subroute and gets the event with specified id.

    :param id: The id of the event to read.
    :type id: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The event with specified id.
    :rtype: Event
    """
    event = await repository_events.get_event_by_id(event_id, session)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return event
