from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connect_db import get_session
from src.database.models import User, Role
from src.repository import rates as repository_rates
from src.repository import rate_details as repository_rate_details
from src.schemas.rates import RateBase, RateUpdate, RateResponse
from src.schemas.rate_details import (
    RateDetailModel,
    RateDetailUpdate,
    RateDetailResponse,
)
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/rates", tags=["rates"])

allowed_operations_for_all = RoleAccess([Role.administrator])


@router.post(
    "", response_model=RateResponse, dependencies=[Depends(allowed_operations_for_all)]
)
async def create_rate(
    rate: RateBase,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a POST-operation to create a rate.

    :param rate: The data for the rate to create.
    :type rate: RateBase
    :param session: The database session.
    :type session: AsyncSession
    :return: The newly created rate.
    :rtype: RateResponse
    """
    rate = await repository_rates.create_rate(rate, user, session)
    return rate


@router.get(
    "",
    response_model=List[RateResponse],
    dependencies=[Depends(allowed_operations_for_all)],
)
async def read_rates(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
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
    rate_id: int, rate_update: RateUpdate, session: AsyncSession = Depends(get_session)
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


@router.post(
    "/{rate_id}/rate_details",
    response_model=RateDetailResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def add_rate_detail_to_rate(
    rate_id: UUID4 | int,
    rate_detail_input: RateDetailModel,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a POST-operation to create a rate detail.

    :param rate_id: The ID of the rate to which the rate detail will be added.
    :type rate_id: Union[UUID4, int]
    :param rate_detail_input: The data for the rate detail to create.
    :type rate_detail_input: RateDetailModel
    :param session: The database session.
    :type session: AsyncSession
    :return: The newly created rate detail.
    :rtype: RateDetailResponse
    """
    rate_detail = await repository_rate_details.create_rate_detail(
        rate_id, rate_detail_input, user, session
    )
    return rate_detail


@router.get(
    "/{rate_id}/rate_details",
    response_model=List[RateDetailResponse],
    dependencies=[Depends(allowed_operations_for_all)],
)
async def read_rate_details_for_rate(
    rate_id: UUID4 | int,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a GET-operation to get all rate details for a rate.

    :param rate_id: The ID of the rate for which rate details will be fetched.
    :type rate_id: Union[UUID4, int]
    :param offset: The number of rate details to skip.
    :type offset: int
    :param limit: The maximum number of rate details to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The list of rate details for the specified rate.
    :rtype: List[RateDetailResponse]
    """
    rate_details = await repository_rate_details.read_rate_details_for_rate(
        rate_id, offset, limit, session
    )
    return rate_details


@router.put(
    "/{rate_id}/rate_details/{rate_detail_id}",
    response_model=RateDetailResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def update_rate_detail_for_rate(
    rate_id: UUID4 | int,
    rate_detail_id: int,
    rate_detail_update: RateDetailUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a PUT-operation to update a rate detail for a rate.

    :param rate_id: The ID of the rate for which the rate detail will be updated.
    :type rate_id: Union[UUID4, int]
    :param rate_detail_id: The ID of the rate detail to update.
    :type rate_detail_id: int
    :param rate_detail_update: The updated data for the rate detail.
    :type rate_detail_update: RateDetailUpdate
    :param session: The database session.
    :type session: AsyncSession
    :return: The updated rate detail.
    :rtype: RateDetailResponse
    """
    rate_detail = await repository_rate_details.update_rate_detail_for_rate(
        rate_id, rate_detail_id, rate_detail_update, session
    )
    if not rate_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rate detail not found"
        )
    return rate_detail


@router.delete(
    "/{rate_id}/rate_details/{rate_detail_id}",
    response_model=RateDetailResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def delete_rate_detail_for_rate(
    rate_id: UUID4 | int,
    rate_detail_id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Handles a DELETE-operation to delete a rate detail for a rate.

    :param rate_id: The ID of the rate for which the rate detail will be deleted.
    :type rate_id: Union[UUID4, int]
    :param rate_detail_id: The ID of the rate detail to delete.
    :type rate_detail_id: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The deleted rate detail.
    :rtype: RateDetailResponse
    """
    rate_detail = await repository_rate_details.delete_rate_detail_for_rate(
        rate_id, rate_detail_id, session
    )
    if not rate_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rate detail not found"
        )
    return rate_detail
