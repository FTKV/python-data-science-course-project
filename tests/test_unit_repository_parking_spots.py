import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, ParkingSpot
from src.schemas.parking_spots import ParkingSpotModel, ParkingSpotUpdate, ParkingSpotDB
from src.repository.parking_spots import (
    create_parking_spot,
    update_parking_spot,
    update_parking_spot_available_status,
    delete_parking_spot,
)

class AsyncMockSession:
    def __init__(self):
        self.added_objects = []

    async def commit(self):
        pass

    def delete(self, obj):
        pass

    async def refresh(self, obj):
        pass

    def add(self, obj):
        self.added_objects.append(obj)

    async def execute(self, stmt):
        pass

    async def scalar(self):
        pass


class TestCreateParkingSpot(unittest.IsolatedAsyncioTestCase):
    async def test_create_parking_spot(self):
        user = User(id=1, username="test_user")
        body = ParkingSpotModel(
        title="Test Parking Spot",
        description="Test description",
        )

        # Mocking the AsyncSession
        mock_session = AsyncMockSession()

        created_parking_spot = await create_parking_spot(body, user, mock_session)

        # Verify that the parking spot object was created correctly
        self.assertIsInstance(created_parking_spot, ParkingSpot)
        self.assertEqual(created_parking_spot.title, "Test Parking Spot")
        self.assertEqual(created_parking_spot.description, "Test description")
        self.assertEqual(created_parking_spot.user_id, user.id)


class TestUpdateParkingSpot(unittest.IsolatedAsyncioTestCase):
    async def test_update_parking_spot_not_found(self):
        # Given
        parking_spot_id = UUID('123e4567-e89b-12d3-a456-426614174000')
        new_parking_spot = ParkingSpotUpdate(
            title="Updated Parking Spot",
            description="Updated description",
            is_available=True,
            is_out_of_service=False
        )

        mock_session = AsyncMockSession()
        mock_session.commit = MagicMock()
        mock_session.refresh = MagicMock()

        # Mocking the get_parking_spot_by_id function to return None
        with patch("src.repository.parking_spots.get_parking_spot_by_id", return_value=None):
            updated_parking_spot = await update_parking_spot(parking_spot_id, new_parking_spot, mock_session)

        self.assertIsNone(updated_parking_spot)
        mock_session.commit.assert_not_called()
        mock_session.refresh.assert_not_called()


class TestUpdateParkingSpotAvailability(unittest.IsolatedAsyncioTestCase):
    async def test_update_parking_spot_available_status_found(self):
        parking_spot_id = UUID('123e4567-e89b-12d3-a456-426614174000')
        available = True

        mock_parking_spot = ParkingSpot(
            id=parking_spot_id,
            title="Test Parking Spot",
            description="Test description",
            is_available=False,
            is_out_of_service=False
        )

        mock_session = AsyncMockSession()

        with patch("src.repository.parking_spots.get_parking_spot_by_id", return_value=mock_parking_spot):
            updated_parking_spot = await update_parking_spot_available_status(parking_spot_id, available, mock_session)

        self.assertEqual(updated_parking_spot, mock_parking_spot)
        self.assertEqual(updated_parking_spot.is_available, available)

    async def test_update_parking_spot_available_status_not_found(self):
        parking_spot_id = UUID('123e4567-e89b-12d3-a456-426614174000')
        available = True

        mock_session = AsyncMockSession()

        with patch("src.repository.parking_spots.get_parking_spot_by_id", return_value=None):
            updated_parking_spot = await update_parking_spot_available_status(parking_spot_id, available, mock_session)

        self.assertIsNone(updated_parking_spot)


class TestDeleteParkingSpot(unittest.IsolatedAsyncioTestCase):
    @patch("src.repository.parking_spots.get_parking_spot_by_id")
    async def test_delete_parking_spot_success(self, mock_get_parking_spot_by_id):
        parking_spot_id = UUID('123e4567-e89b-12d3-a456-426614174000')
        mock_parking_spot = ParkingSpot(id=parking_spot_id, title="Test Parking Spot", description="Test description")

        mock_session = AsyncMockSession()

        # Patching the commit method
        with patch.object(mock_session, "commit") as mock_commit:
            mock_get_parking_spot_by_id.return_value = mock_parking_spot

            result = await delete_parking_spot(parking_spot_id, mock_session)

            self.assertTrue(result)
            mock_commit.assert_called_once()

    @patch("src.repository.parking_spots.get_parking_spot_by_id")
    async def test_delete_parking_spot_failure(self, mock_get_parking_spot_by_id):
        parking_spot_id = UUID('123e4567-e89b-12d3-a456-426614174000')

        mock_session = AsyncMockSession()

        # Patching the commit method
        with patch.object(mock_session, "commit") as mock_commit:
            mock_get_parking_spot_by_id.return_value = None

            result = await delete_parking_spot(parking_spot_id, mock_session)

            self.assertFalse(result)
            mock_commit.assert_not_called()


if  __name__=='__main__':
    unittest.main()