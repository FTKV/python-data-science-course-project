import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Car
from src.schemas.cars import (
    CarRecognizedPlateModel,
    CarUpdateModel,
)
from src.repository.cars import (
    create_car,
    read_cars,
    read_cars_by_user_id,
    read_car_by_car_id,
    read_car_by_plate,
    update_car,
    block_or_unblock_car,
    is_car_blocked,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.user = User(
            id=1,
            username="test",
            email="test@test.com",
            password="1234567890",
        )
        self.car = Car(id=1, plate="ABC12345", is_blocked=False, user_id=1)
        self.body = CarRecognizedPlateModel(plate="ABC12345")
        self.new_body = CarUpdateModel(plate="XYZ67890")
        self.session = MagicMock(spec=AsyncSession)

    async def test_create_car(self):
        result = await create_car(
            body=self.body,
            session=self.session,
        )
        self.assertEqual(result.plate, self.body.plate)
        self.assertFalse(result.is_blocked)

    async def test_read_cars(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalars.return_value = [self.car]
        result = await read_cars(0, 10, self.session)
        self.assertEqual(result[0], self.car)

    async def test_read_cars_by_user_id(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalars.return_value = [self.car]
        result = await read_cars_by_user_id(
            user_id=self.car.user_id,
            offset=0,
            limit=10,
            session=self.session,
        )
        self.assertEqual(result[0], self.car)

    async def test_read_cars_by_car_id(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalar.return_value = self.car
        result = await read_car_by_car_id(
            car_id=self.car.id,
            session=self.session,
        )
        self.assertEqual(result, self.car)

    async def test_read_cars_by_plate(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalar.return_value = self.car
        result = await read_car_by_plate(
            plate=self.car.plate,
            session=self.session,
        )
        self.assertEqual(result, self.car)

    async def test_update_car(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalar.return_value = self.car
        result = await update_car(
            car_id=self.car.id,
            body=self.new_body,
            session=self.session,
        )
        self.assertEqual(result, self.car)

    async def test_block_or_unblock_car(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalar.return_value = self.car
        result = await block_or_unblock_car(
            car_id=self.car.id,
            is_to_block=True,
            session=self.session,
        )
        self.assertTrue(result.is_blocked)

    async def test_is_car_blocked(self):
        self.session.execute.return_value = MagicMock(spec=ChunkedIteratorResult)
        self.session.execute.return_value.scalar.return_value = self.car
        await block_or_unblock_car(
            car_id=self.car.id,
            is_to_block=True,
            session=self.session,
        )
        result = await is_car_blocked(
            plate=self.car.plate,
            session=self.session,
        )
        self.assertTrue(result)
