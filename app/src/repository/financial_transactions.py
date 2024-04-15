"""
Module of financial transactions' CRUD
"""

from sqlalchemy import select, UUID
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import settings
from src.database.models import User, FinancialTransaction
from src.schemas.financial_transactions import FinancialTransactionModel
from src.services.cloudinary import cloudinary_service


async def create_financial_transaction(
    body: FinancialTransactionModel, session: AsyncSession
) -> FinancialTransaction:
    """
    Creates a new financial transaction.

    :param body: The body for the financial transaction to create.
    :type body: FinancialTransactionModel
    :param session: The database session.
    :type session: AsyncSession
    :return: The newly created financial transaction.
    :rtype: FinancialTransaction
    """
    financial_transaction = FinancialTransaction(**body.model_dump())
    session.add(financial_transaction)
    await session.commit()
    await session.refresh(financial_transaction)
    return financial_transaction


async def read_financial_transactions(
    offset: int, limit: int, session: AsyncSession
) -> ScalarResult:
    """
    Gets all financial transactions.

    :param offset: The number of financial transactions to skip.
    :type offset: int
    :param limit: The maximum number of financial transactions to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The ScalarResult with the list of financial transactions.
    :rtype: ScalarResult
    """
    stmt = select(FinancialTransaction)
    stmt = stmt.offset(offset).limit(limit)
    financial_transactions = await session.execute(stmt)
    return financial_transactions.scalars()


async def read_financial_transactions_by_user_id(
    user_id: UUID | int, offset: int, limit: int, session: AsyncSession
) -> ScalarResult:
    """
    Gets financial transactions by user with the specified id.

    :param user_id: The ID of the user to get financial transactions.
    :type user_id: UUID | int
    :param offset: The number of financial transactions to skip.
    :type offset: int
    :param limit: The maximum number of financial transactions to return.
    :type limit: int
    :param session: The database session.
    :type session: AsyncSession
    :return: The ScalarResult with the list of financial transactions.
    :rtype: ScalarResult
    """
    stmt = select(FinancialTransaction).filter(FinancialTransaction.user_id == user_id)
    stmt = stmt.offset(offset).limit(limit)
    financial_transactions = await session.execute(stmt)
    return financial_transactions.scalars()


async def read_financial_transaction(
    fin_trans_id: UUID | int,
    session: AsyncSession,
) -> FinancialTransaction | None:
    """
    Gets a financial transaction with the specified id.

    :param fin_trans_id: The ID of the financial transaction to get.
    :type fin_trans_id: UUID | int
    :param session: The database session.
    :type session: AsyncSession
    :return: The financial transaction with the specified ID, or None if it does not exist.
    :rtype: FinancialTransaction | None
    """
    stmt = select(FinancialTransaction).filter(FinancialTransaction.id == fin_trans_id)
    financial_transaction = await session.execute(stmt)
    return financial_transaction.scalar()
