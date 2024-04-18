import unittest
from unittest.mock import MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Reservation
from src.schemas.reservations import ReservationModel, ReservationUpdateModel
from src.repository.reservations import (
    create_reservation,
    get_reservation_by_id,
    get_reservations_by_user_id,
    get_all_reservations,
    update_reservation,
    get_debit_credit_of_reservation,
)

class MockRedis:
    async def get(*args):
        pass

    async def set(*args):
        pass

    async def expire(*args):
        pass

class TestReservations(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.reservation_data = ReservationModel(
            resv_status="CHECKED_IN",
            start_date="2024-04-20 08:00:00",
            end_date="2024-04-20 18:00:00",
            user_id=1,
            parking_spot_id=1,
            car_id=1,
            rate_id=1,
        )
        self.update_data = ReservationUpdateModel(
            resv_status="CHECKED_OUT",
            start_date="2024-04-20 09:00:00",
            end_date="2024-04-20 17:00:00",
            debit=50.00,
            credit=0.00,
            user_id=1,
            parking_spot_id=1,
            rate_id=2,
        )
        self.session = MagicMock(spec=AsyncSession)

    async def test_create_reservation(self):
        reservation = await create_reservation(self.reservation_data, self.session)
        self.assertIsInstance(reservation, Reservation)

    async def test_create_reservation_missing_user_id(self):
        self.reservation_data.user_id = None
        with self.assertRaises(ValueError):
            await create_reservation(self.reservation_data, self.session)

    async def test_get_reservation_by_id_existing(self):
        self.session.execute.return_value.scalar.return_value = Reservation()
        reservation = await get_reservation_by_id(1, self.session)
        self.assertIsInstance(reservation, Reservation)

    async def test_get_reservation_by_id_non_existing(self):
        self.session.execute.return_value.scalar.return_value = None
        reservation = await get_reservation_by_id(999, self.session)
        self.assertIsNone(reservation)

    async def test_get_reservations_by_user_id(self):
        self.session.execute.return_value.scalars.return_value.all.return_value = [
            Reservation()
        ]
        reservations = await get_reservations_by_user_id(1, 0, 10, self.session)
        self.assertIsInstance(reservations, list)
        self.assertEqual(len(reservations), 1)

    async def test_get_all_reservations(self):
        self.session.execute.return_value.scalars.return_value.all.return_value = [
            Reservation()
        ]
        reservations = await get_all_reservations(0, 10, self.session)
        self.assertIsInstance(reservations, list)
        self.assertEqual(len(reservations), 1)

    async def test_update_reservation_existing(self):
        self.session.execute.return_value.scalar.return_value = Reservation()
        updated_reservation = await update_reservation(1, self.update_data, self.session)
        self.assertIsInstance(updated_reservation, Reservation)

    async def test_update_reservation_non_existing(self):
        self.session.execute.return_value.scalar.return_value = None
        updated_reservation = await update_reservation(999, self.update_data, self.session)
        self.assertIsNone(updated_reservation)

    async def test_get_debit_credit_of_reservation(self):
        self.session.execute.return_value.all.return_value = [(50.0, 0.0)]
        debit, credit = await get_debit_credit_of_reservation(1, self.session)
        self.assertEqual(debit, 50.0)
        self.assertEqual(credit, 0.0)


if __name__ == "__main__":
    unittest.main()
