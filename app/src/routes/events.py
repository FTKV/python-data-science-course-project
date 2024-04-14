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
from src.database.models import Event, Role
from src.repository import events as repository_events
from src.services.auth import auth_service
from src.services.roles import RoleAccess
from src.schemas.events import EventModel, EventDB


router = APIRouter(prefix="/events", tags=["events"])

allowed_operations_for_self = RoleAccess([Role.administrator, Role.user])
allowed_operations_for_all = RoleAccess([Role.administrator])


@router.post("/make", status_code=status.HTTP_201_CREATED, dependencies=[Depends(allowed_operations_for_all)])
async def create_event(
    body: EventModel,
    # current_user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
    cache: Redis = Depends(get_redis_db1),
):
    """
    Handles a POST-operation to "{id}" event subroute and create an event.

    :param body: The data for the event to create.
    :type body: EventModel
    :type AsyncSession: The current session.
    :return: Newly created event.
    :rtype: Event
    """
    # :param user: The user who creates the image.
    # :type user: User
    # :param session: Get the database session

    event = await repository_events.create_event(body, session)
    return event


@router.get(
    "/{id}",
    response_model=EventDB,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def read_event(id: int, session: AsyncSession = Depends(get_session), cache: Redis = Depends(get_redis_db1)):
    """
    Handles a GET-operation to '/{id}' event subroute and gets the user's profile with specified username.

    :param id: The id of the event to read.
    :type id: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The event with specified id.
    :rtype: Event
    """
    event = await repository_events.get_event_by_id(id, session)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return event