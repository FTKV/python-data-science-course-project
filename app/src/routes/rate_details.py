from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connect_db import get_session
from src.database.models import Role
from src.repository import rate_details as repository_rate_details
from src.schemas.rate_details import (
    RateDetailInput,
    RateDetailUpdate,
    RateDetailResponse,
)
from src.services.roles import RoleAccess


router = APIRouter(prefix="/rate-details", tags=["rate-details"])

allowed_operations_for_all = RoleAccess([Role.administrator])


@router.post(
    "",
    response_model=RateDetailResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def create_rate_detail(
    rate_detail_input: RateDetailInput, session: AsyncSession = Depends(get_session)
):
    """
    Handles a POST-operation to create a rate detail.

    :param rate_detail_input: The data for the rate detail to create.
    :type rate_detail_input: RateDetailInput
    :param session: The database session.
    :type session: AsyncSession
    :return: The newly created rate detail.
    :rtype: RateDetailResponse
    """
    rate_detail = await repository_rate_details.create_rate_detail(
        rate_detail_input, session
    )
    return rate_detail


@router.get("", response_model=List[RateDetailResponse], dependencies=[Depends(allowed_operations_for_all)])
async def read_rate_details(
    offset: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)
):
    """
    Handles a GET-operation to get all rate details.

    :param offset: The number of rate details to skip.
    :type offset: int
    :param limit: The maximum number of rate details to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The list of rate details.
    :rtype: List[RateDetailResponse]
    """
    rate_details = await repository_rate_details.read_rate_details(
        offset, limit, session
    )
    return rate_details


@router.put("/{rate_detail_id}", response_model=RateDetailResponse, dependencies=[Depends(allowed_operations_for_all)])
async def update_rate_detail(
    rate_detail_id: int,
    rate_detail_update: RateDetailUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a PUT-operation to update a rate detail.

    :param rate_detail_id: The ID of the rate detail to update.
    :type rate_detail_id: int
    :param rate_detail_update: The updated data for the rate detail.
    :type rate_detail_update: RateDetailUpdate
    :param session: The database session.
    :type session: AsyncSession
    :return: The updated rate detail.
    :rtype: RateDetailResponse
    """
    rate_detail = await repository_rate_details.update_rate_detail(
        rate_detail_id, rate_detail_update, session
    )
    if not rate_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rate detail not found"
        )
    return rate_detail


@router.delete("/{rate_detail_id}", response_model=RateDetailResponse, dependencies=[Depends(allowed_operations_for_all)])
async def delete_rate_detail(
    rate_detail_id: int, session: AsyncSession = Depends(get_session)
):
    """
    Handles a DELETE-operation to delete a rate detail.

    :param rate_detail_id: The ID of the rate detail to delete.
    :type rate_detail_id: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The deleted rate detail.
    :rtype: RateDetailResponse
    """
    rate_detail = await repository_rate_details.delete_rate_detail(
        rate_detail_id, session
    )
    if not rate_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rate detail not found"
        )
    return rate_detail
