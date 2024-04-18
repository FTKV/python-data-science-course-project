import unittest
from unittest.mock import AsyncMock, MagicMock

from app.src.database.models import Reservation
from app.src.schemas.reservations import ReservationModel
from app.src.repository.reservations import (
    create_reservation,
    get_all_reservations,
    get_debit_credit_of_reservation,
)


class TestReservations(unittest.TestCase):
    def setUp(self):
        self.session = AsyncMock()
        self.reservation_data = ReservationModel(
            resv_status="CHECKED_IN",
            start_date="2024-04-20 08:00:00",
            end_date="2024-04-20 18:00:00",
            user_id=1,
            parking_spot_id=1,
            car_id=1,
            rate_id=1,
        )

    async def test_create_reservation(self):
        self.session.execute.return_value.scalar.return_value = Reservation()
        reservation = await create_reservation(self.reservation_data, self.session)
        self.assertIsInstance(reservation, Reservation)

    async def test_get_all_reservations(self):
        self.session.execute.return_value.scalars.return_value.all.return_value = [Reservation()]
        reservations = await get_all_reservations(0, 10, self.session)
        self.assertIsInstance(reservations, list)

    async def test_get_debit_credit_of_reservation(self):
        result = MagicMock()
        result.all.return_value = [(50.0, 0.0)]
        self.session.execute.return_value = result
        debit, credit = await get_debit_credit_of_reservation(1, self.session)
        self.assertEqual(debit, 50.0)
        self.assertEqual(credit, 0.0)


if __name__ == "__main__":
    unittest.main()
