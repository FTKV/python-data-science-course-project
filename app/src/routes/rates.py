from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connect_db import get_session
from src.database.models import Role
from src.repository import rates as repository_rates
from src.schemas.rates import (
    RateInput,
    RateUpdate,
    RateResponse,
)
from src.services.roles import RoleAccess


router = APIRouter(prefix="/rates", tags=["rates"])

allowed_operations_for_all = RoleAccess([Role.administrator])


@router.post(
    "",
    response_model=RateResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def create_rate(
    rate_input: RateInput, session: AsyncSession = Depends(get_session)
):
    """
    Handles a POST-operation to create a rate.

    :param rate_input: The data for the rate to create.
    :type rate_input: RateInput
    :param session: The database session.
    :type session: AsyncSession
    :return: The newly created rate.
    :rtype: RateResponse
    """
    rate = await repository_rates.create_rate(rate_input, session)
    return rate


@router.get(
    "",
    response_model=List[RateResponse],
    dependencies=[Depends(allowed_operations_for_all)],
)
async def read_rates(
    offset: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)
):
    """
    Handles a GET-operation to get all rates.

    :param offset: The number of rates to skip.
    :type offset: int
    :param limit: The maximum number of rates to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The list of rates.
    :rtype: List[RateResponse]
    """
    rates = await repository_rates.read_rates(offset, limit, session)
    return rates


@router.put(
    "/{rate_id}",
    response_model=RateResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def update_rate(
    rate_id: int,
    rate_update: RateUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a PUT-operation to update a rate.

    :param rate_id: The ID of the rate to update.
    :type rate_id: int
    :param rate_update: The updated data for the rate.
    :type rate_update: RateUpdate
    :param session: The database session.
    :type session: AsyncSession
    :return: The updated rate.
    :rtype: RateResponse
    """
    rate = await repository_rates.update_rate(rate_id, rate_update, session)
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rate not found"
        )
    return rate


@router.delete(
    "/{rate_id}",
    response_model=RateResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def delete_rate(rate_id: int, session: AsyncSession = Depends(get_session)):
    """
    Handles a DELETE-operation to delete a rate.

    :param rate_id: The ID of the rate to delete.
    :type rate_id: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The deleted rate.
    :rtype: RateResponse
    """
    rate = await repository_rates.delete_rate(rate_id, session)
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rate not found"
        )
    return rate
