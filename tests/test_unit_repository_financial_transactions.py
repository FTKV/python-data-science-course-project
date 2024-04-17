import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, TrxType, FinancialTransaction
from src.schemas.financial_transactions import FinancialTransactionModel
from src.repository.financial_transactions import (
    create_financial_transaction,
    read_financial_transactions,
    read_financial_transactions_by_user_id,
    read_financial_transaction,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.user = User(
            id=1,
            username="test",
            email="test@test.com",
            password="1234567890",
        )
        self.financial_transaction = FinancialTransaction(
            id=1,
            trx_type=TrxType.PAYMENT,
            debit=0.0,
            credit=100.0,
            user_id=1,
            reservation_id=1,
        )
        self.body = FinancialTransactionModel(
            trx_type=TrxType.PAYMENT,
            debit=0.0,
            credit=100.0,
            user_id=1,
            reservation_id=1,
        )
        self.session = MagicMock(spec=AsyncSession)

    async def test_create_car(self):
        result = await create_financial_transaction(
            body=self.body,
            session=self.session,
        )
        self.assertEqual(result.trx_type, self.body.trx_type)
        self.assertEqual(result.credit, self.body.credit)

    async def test_read_financial_transactions(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalars.return_value = [
            self.financial_transaction
        ]
        result = await read_financial_transactions(0, 10, self.session)
        self.assertEqual(result[0], self.financial_transaction)

    async def test_read_financial_transactions_by_user_id(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalars.return_value = [
            self.financial_transaction
        ]
        result = await read_financial_transactions_by_user_id(
            user_id=self.financial_transaction.user_id,
            offset=0,
            limit=10,
            session=self.session,
        )
        self.assertEqual(result[0], self.financial_transaction)

    async def test_read_financial_transaction(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalar.return_value = (
            self.financial_transaction
        )
        result = await read_financial_transaction(
            fin_trans_id=self.financial_transaction.id,
            session=self.session,
        )
        self.assertEqual(result, self.financial_transaction)
