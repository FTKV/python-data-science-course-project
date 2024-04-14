"""
Module of events' CRUD
"""

from sqlalchemy import select, UUID
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import settings
from src.database.models import User, Event
from src.schemas.events import EventModel


async def create_event(body: EventModel, session: AsyncSession) -> Event:
    """
    Creates a new event.

    :param body: The body for the event to create.
    :type body: EventModel
    :param session: The database session.
    :type session: AsyncSession
    :return: The newly created event.
    :rtype: Event
    """
    event = Event(**body.model_dump())
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


async def get_event_by_id(
    event_id: UUID | int,
    session: AsyncSession,
) -> Event | None:
    """
    Gets an event with the specified id.

    :param event_id: The ID of the event to get.
    :type event_id: UUID | int
    :param session: The database session.
    :type session: AsyncSession
    :return: The event with the specified ID, or None if it does not exist.
    :rtype: Event | None
    """
    stmt = select(Event).filter(Event.id == event_id)
    event = await session.execute(stmt)
    return event.scalar()