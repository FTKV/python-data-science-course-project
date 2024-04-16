import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import MagicMock

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.models import User, ParkingSpot
from app.src.schemas.parking_spots import ParkingSpotModel, ParkingSpotUpdate, ParkingSpotDB
from app.src.repository.parking_spots import (
    create_parking_spot,
    get_parking_spot_by_id,
    update_parking_spot,
    update_parking_spot_available_status,
    delete_parking_spot,
    get_all_parking_spots,
    update_parking_spot_service_status,
)

class TestParkingSpot(unittest.IsolatedAsyncioTestCase):
    async def test_create_parking_spot(self):
        user = User(id=1, username="test_user")
        body = ParkingSpotModel(
        name="Test Parking Spot",
        description="Test description",
        )
        

        # Mocking the AsyncSession
        mock_session = MagicMock(spec=AsyncSession)
        mock_commit = MagicMock()
        mock_session.commit = mock_commit

        # When
        created_parking_spot = await create_parking_spot(body, user, mock_session)

        # Then
        # Verify that the parking spot object was created correctly
        self.assertIsInstance(created_parking_spot, ParkingSpot)
        self.assertEqual(created_parking_spot.name, "Test Parking Spot")
        self.assertEqual(created_parking_spot.description, "Test description")
        self.assertEqual(created_parking_spot.latitude, 123.456)
        self.assertEqual(created_parking_spot.longitude, 456.789)
        self.assertEqual(created_parking_spot.user_id, user.id)

        # Verify that the session's commit method was called
        mock_commit.assert_called_once()
