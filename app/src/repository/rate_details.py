from sqlalchemy import select, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import RateDetail
from src.schemas.rate_details import RateDetailInput, RateDetailUpdate, RateDetailResponse
from typing import List

async def create_rate_detail(body: RateDetailInput, session: AsyncSession) -> RateDetail:
    """
    Creates a new rate detail.

    :param body: The body for the rate detail to create.
    :type body: RateDetailInput
    :param session: The database session.
    :type session: AsyncSession
    :return: The newly created rate detail.
    :rtype: RateDetail
    """
    rate_detail = RateDetail(**body.dict())
    session.add(rate_detail)
    await session.commit()
    await session.refresh(rate_detail)
    return rate_detail

async def read_rate_details(offset: int, limit: int, session: AsyncSession) -> List[RateDetail]:
    """
    Gets all rate details.

    :param offset: The number of rate details to skip.
    :type offset: int
    :param limit: The maximum number of rate details to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The list of rate details.
    :rtype: List[RateDetail]
    """
    stmt = select(RateDetail).offset(offset).limit(limit)
    rate_details = await session.execute(stmt)
    return rate_details.scalars().all()

async def read_rate_detail_by_id(rate_detail_id: int, session: AsyncSession) -> RateDetail | None:
    """
    Gets a rate detail by ID.

    :param rate_detail_id: The ID of the rate detail to get.
    :type rate_detail_id: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The rate detail with the specified ID, or None if it does not exist.
    :rtype: RateDetail | None
    """
    stmt = select(RateDetail).filter(RateDetail.id == rate_detail_id)
    rate_detail = await session.execute(stmt)
    return rate_detail.scalar()

async def update_rate_detail(rate_detail_id: int, body: RateDetailUpdate, session: AsyncSession) -> RateDetail | None:
    """
    Updates a rate detail.

    :param rate_detail_id: The ID of the rate detail to update.
    :type rate_detail_id: int
    :param body: The updated body for the rate detail.
    :type body: RateDetailUpdate
    :param session: The database session.
    :type session: AsyncSession
    :return: The updated rate detail, or None if it does not exist.
    :rtype: RateDetail | None
    """
    rate_detail = await read_rate_detail_by_id(rate_detail_id, session)
    if rate_detail:
        for key, value in body.dict().items():
            setattr(rate_detail, key, value)
        await session.commit()
    return rate_detail

async def delete_rate_detail(rate_detail_id: int, session: AsyncSession) -> RateDetail | None:
    """
    Deletes a rate detail.

    :param rate_detail_id: The ID of the rate detail to delete.
    :type rate_detail_id: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The deleted rate detail, or None if it does not exist.
    :rtype: RateDetail | None
    """
    rate_detail = await read_rate_detail_by_id(rate_detail_id, session)
    if rate_detail:
        session.delete(rate_detail)
        await session.commit()
    return rate_detail
