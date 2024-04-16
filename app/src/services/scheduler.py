from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.database.connect_db import get_session
from src.database.models import TrxType
from src.repository import cars as repository_cars
from src.repository import financial_transactions as repository_financial_transactions
from src.repository import rates as repository_rates
from src.repository import reservations as repository_reservations
from src.schemas.financial_transactions import FinancialTransactionModel
from src.schemas.reservations import ReservationUpdateModel


scheduler = AsyncIOScheduler(
    # jobstores={
    #     "default": RedisJobStore(db=2, host="127.0.0.1", port=6379, password="test")
    # }
)


@scheduler.scheduled_job("cron", second=0)
async def make_charges_to_in_house_reservations():
    async for session in get_session():
        reservations = await repository_reservations.get_all_in_house_reservations(
            session
        )
        for reservation in reservations.all():
            amount = await repository_rates.get_rate_amount(
                reservation.rate_id, session
            )
            if not reservation.user_id:
                car = await repository_cars.read_car_by_car_id(
                    reservation.car_id, session
                )
                if car.user_id:
                    reservation.user_id = car.user_id
            data = FinancialTransactionModel(
                trx_type=TrxType.CHARGE,
                debit=amount,
                credit=0.0,
                user_id=reservation.user_id,
                reservation_id=reservation.id,
            )
            financial_transaction = (
                await repository_financial_transactions.create_financial_transaction(
                    data, session
                )
            )
            debit, credit = (
                await repository_reservations.get_debit_credit_of_reservation(
                    financial_transaction.reservation_id, session
                )
            )
            data = ReservationUpdateModel(debit=debit, credit=credit)
            await repository_reservations.update_reservation(
                financial_transaction.reservation_id, data, session
            )
