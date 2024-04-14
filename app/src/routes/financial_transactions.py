"""
Module of users' routes
"""

from pydantic import UUID4
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from redis.asyncio.client import Redis
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connect_db import get_session, get_redis_db1
from src.database.models import User, Role
from src.repository import financial_transactions as repository_financial_transactions
from src.repository import reservations as repository_reservations
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.roles import RoleAccess
from src.schemas.financial_transactions import (
    FinancialTransactionModel,
    FinancialTransactionResponse,
)
from src.schemas.reservations import ReservationUpdateModel


router = APIRouter(prefix="/fin_trans", tags=["fin_trans"])

allowed_operations_for_self = RoleAccess([Role.administrator, Role.user])
allowed_operations_for_all = RoleAccess([Role.administrator])


@router.post(
    "",
    response_model=FinancialTransactionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def create_financial_transaction(
    body: FinancialTransactionModel,
    session: AsyncSession = Depends(get_session),
):
    financial_transaction = (
        await repository_financial_transactions.create_financial_transaction(
            body, session
        )
    )
    result = await repository_reservations.get_debit_credit_of_reservation(
        financial_transaction.reservation_id, session
    )
    debit, credit = result[0]
    body = ReservationUpdateModel(debit=debit, credit=credit)
    await repository_reservations.update_reservation(
        financial_transaction.reservation_id, body, session
    )
    return financial_transaction


@router.get(
    "",
    response_model=FinancialTransactionResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def read_financial_transaction(
    fin_trans_id: UUID4 | int,
    session: AsyncSession = Depends(get_session),
) -> ScalarResult:
    """
    Handles a GET-operation to financial_transactions route and gets a financial transaction with the specified id.

    :param fin_trans_id: The ID of the financial transaction to get.
    :type fin_trans_id: UUID4 | int
    :param session: The database session.
    :type session: AsyncSession
    :return: The financial transaction with the specified ID, or None if it does not exist.
    :rtype: FinancialTransaction | None
    """
    financial_transaction = (
        await repository_financial_transactions.read_financial_transaction(
            fin_trans_id, session
        )
    )
    if not financial_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial transaction not found",
        )
    return financial_transaction


@router.get(
    "/all",
    response_model=List[FinancialTransactionResponse],
    dependencies=[Depends(allowed_operations_for_all)],
)
async def read_financial_transactions(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
) -> ScalarResult:
    """
    Handles a GET-operation to "/all" financial_transactions subroute and gets all financial transactions.

    :param offset: The number of financial transactions to skip.
    :type offset: int
    :param limit: The maximum number of financial transactions to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The ScalarResult with the list of financial transactions.
    :rtype: ScalarResult
    """
    financial_transactions = (
        await repository_financial_transactions.read_financial_transactions(
            offset, limit, session
        )
    )
    return financial_transactions
