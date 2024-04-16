from pydantic import UUID4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User, Rate, RateDetail
from src.schemas.rates import RateModel, RateUpdate
from typing import List


DEFAULT_RATE = "DEFAULT"


async def create_rate(body: RateModel, user: User, session: AsyncSession) -> Rate:
    """
    Creates a new rate.
    :param body: The body for the rate to create.
    :type body: RateModel
    :param session: The database session.
    :type session: AsyncSession
    :return: The newly created rate.
    :rtype: Rate
    """
    rate = Rate(**body.model_dump(), user_id=user.id)
    session.add(rate)
    await session.commit()
    await session.refresh(rate)
    return rate


async def read_rates(offset: int, limit: int, session: AsyncSession) -> List[Rate]:
    """
    Gets all rates.
    :param offset: The number of rates to skip.
    :type offset: int
    :param limit: The maximum number of rates to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The list of rates.
    :rtype: List[Rate]
    """
    stmt = select(Rate).offset(offset).limit(limit)
    rates = await session.execute(stmt)
    return rates.scalars()


async def read_rate_by_id(rate_id: UUID4 | int, session: AsyncSession) -> Rate | None:
    """
    Gets a rate by ID.
    :param rate_id: The ID of the rate to get.
    :type rate_id: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The rate with the specified ID, or None if it does not exist.
    :rtype: Rate | None
    """
    stmt = select(Rate).filter(Rate.id == rate_id)
    rate = await session.execute(stmt)
    return rate.scalar()


async def update_rate(
    rate_id: UUID4 | int, body: RateUpdate, session: AsyncSession
) -> Rate | None:
    """
    Updates a rate.
    :param rate_id: The ID of the rate to update.
    :type rate_id: UUID4 | int
    :param body: The updated body for the rate.
    :type body: RateUpdate
    :param session: The database session.
    :type session: AsyncSession
    :return: The updated rate, or None if it does not exist.
    :rtype: Rate | None
    """
    rate = await read_rate_by_id(rate_id, session)
    if rate:
        for key, value in body.model_dump().items():
            if hasattr(rate, key) and value is not None:
                setattr(rate, key, value)
        await session.commit()
    return rate


async def delete_rate(rate_id: UUID4 | int, session: AsyncSession) -> Rate | None:
    """
    Deletes a rate.
    :param rate_id: The ID of the rate to delete.
    :type rate_id: UUID4 | int
    :param session: The database session.
    :type session: AsyncSession
    :return: The deleted rate, or None if it does not exist.
    :rtype: Rate | None
    """
    rate = await read_rate_by_id(rate_id, session)
    if rate:
        session.delete(rate)
        await session.commit()
    return rate


async def get_default_rate(session: AsyncSession) -> Rate | None:
    stmt = select(Rate).filter(Rate.title == DEFAULT_RATE)
    rate = await session.execute(stmt)
    return rate.scalar()


async def get_rate_amount(rate_id: UUID4 | int, session: AsyncSession):
    rate = await read_rate_by_id(rate_id, session)
    stmt = select(RateDetail).filter(RateDetail.rate_id == rate.id)
    rate_details = await session.execute(stmt)
    rate_detail = rate_details.scalar()
    return rate_detail.amount
