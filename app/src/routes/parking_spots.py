from pydantic import UUID4
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connect_db import get_session
from src.services.auth import auth_service
from src.services.roles import RoleAccess
from src.database.models import User, Role
from src.repository.parking_spots import (
    create_parking_spot,
    get_parking_spot_by_id,
    update_parking_spot,
    update_parking_spot_available_status,
    delete_parking_spot,
    get_all_parking_spots,
    update_parking_spot_service_status,
)
from src.schemas.parking_spots import (
    ParkingSpotModel,
    ParkingSpotResponse,
    ParkingSpotUpdate,
)

router = APIRouter(prefix="/parking_spots", tags=["parking_spots"])

allowed_operations_for_all = RoleAccess([Role.administrator])
allowed_operations_for_self = RoleAccess([Role.administrator, Role.user])


@router.post(
    "",
    response_model=ParkingSpotResponse,
    dependencies=[Depends(allowed_operations_for_all)],
    status_code=status.HTTP_201_CREATED,
)
async def create_parking_spot_route(
    data: ParkingSpotModel = Depends(ParkingSpotModel.as_form),
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new parking spot.

    This endpoint allows administrators to create a new parking spot. Only users with
    the role of administrator have permission to access this endpoint.

    Args:
        data (ParkingSpotModel): The data to create the parking spot.
        user (User, optional): The current user accessing the endpoint. Defaults to
            Depends(auth_service.get_current_user).
        session (AsyncSession, optional): The asynchronous session to interact with
            the database. Defaults to Depends(get_session).

    Returns:
        dict: The created parking spot along with a success message.

    Raises:
        HTTPException: If the current user is not authorized to access the endpoint.
    """
    parking_spot = await create_parking_spot(data, user, session)
    return {"user": parking_spot, "message": "Parking spot created successfully"}


@router.get(
    "/{parking_spot_id}",
    response_model=ParkingSpotResponse,
    dependencies=[Depends(allowed_operations_for_self)],
)
async def get_parking_spot_route(
    parking_spot_id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Retrieve a parking spot by ID.

    This endpoint allows users to retrieve a parking spot by providing its ID.
    Only users with specific permissions (determined by `allowed_operations_for_self`)
    have access to this endpoint.

    Args:
        parking_spot_id (int): The ID of the parking spot to retrieve.
        session (AsyncSession, optional): The asynchronous session to interact with
            the database. Defaults to Depends(get_session).

    Returns:
        dict: The retrieved parking spot along with a success message.

    Raises:
        HTTPException: If the parking spot with the provided ID is not found.
    """
    parking_spot = await get_parking_spot_by_id(session, parking_spot_id)
    if not parking_spot:
        raise HTTPException(status_code=404, detail="Parking spot not found")
    return {"user": parking_spot, "message": "Parking spot retrieved successfully"}


@router.put(
    "/{parking_spot_id}",
    response_model=ParkingSpotResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def update_parking_spot_route(
    parking_spot_id: int,
    data: ParkingSpotUpdate = Depends(ParkingSpotUpdate.as_form),
    session: AsyncSession = Depends(get_session),
):
    """
    Update a parking spot by ID.

    This endpoint allows administrators to update a parking spot by providing its ID
    and the updated data in the request body. Only users with specific permissions
    (determined by `allowed_operations_for_all`) have access to this endpoint.

    Args:
        parking_spot_id (int): The ID of the parking spot to update.
        data (ParkingSpotUpdate): The updated data for the parking spot.
        session (AsyncSession, optional): The asynchronous session to interact with
            the database. Defaults to Depends(get_session).

    Returns:
        dict: The updated parking spot along with a success message.

    Raises:
        HTTPException: If the parking spot with the provided ID is not found.
    """
    updated_parking_spot = await update_parking_spot(session, parking_spot_id, data)
    if not updated_parking_spot:
        raise HTTPException(status_code=404, detail="Parking spot not found")
    return {
        "user": updated_parking_spot,
        "message": "Parking spot updated successfully",
    }


@router.patch(
    "/{parking_spot_id}/availability",
    response_model=ParkingSpotResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def update_parking_spot_availability_route(
    parking_spot_id: int,
    available: bool,
    session: AsyncSession = Depends(get_session),
):
    """
    Update the availability status of a parking spot.

    This endpoint allows administrators to update the availability status of a parking spot
    by providing its ID and the new availability status in the request body. Only users with
    specific permissions (determined by `allowed_operations_for_all`) have access to this
    endpoint.

    Args:
        parking_spot_id (int): The ID of the parking spot to update.
        available (bool): The new availability status of the parking spot.
        session (AsyncSession, optional): The asynchronous session to interact with
            the database. Defaults to Depends(get_session).

    Returns:
        dict: The updated parking spot along with a success message.

    Raises:
        HTTPException: If the parking spot with the provided ID is not found.
    """
    updated_parking_spot = await update_parking_spot_available_status(
        session, parking_spot_id, available
    )
    if not updated_parking_spot:
        raise HTTPException(status_code=404, detail="Parking spot not found")
    return {
        "user": updated_parking_spot,
        "message": "Parking spot availability updated successfully",
    }


@router.patch(
    "/{parking_spot_id}/service_status",
    response_model=ParkingSpotResponse,
    dependencies=[Depends(allowed_operations_for_all)],
)
async def update_parking_spot_service_status_route(
    parking_spot_id: int,
    out_of_service: bool,
    session: AsyncSession = Depends(get_session),
):
    """
    Update the service status of a parking spot by ID.

    This endpoint allows administrators to update the service status (in-service or out-of-service)
    of a parking spot by providing its ID and the new service status in the request body.
    Only users with specific permissions (determined by `allowed_operations_for_all`) have access
    to this endpoint.

    Args:
        parking_spot_id (int): The ID of the parking spot to update.
        out_of_service (bool): The new service status of the parking spot.
        session (AsyncSession, optional): The asynchronous session to interact with
            the database. Defaults to Depends(get_session).

    Returns:
        dict: The updated parking spot along with a success message.

    Raises:
        HTTPException: If the parking spot with the provided ID is not found.
    """
    updated_parking_spot = await update_parking_spot_service_status(
        session, parking_spot_id, out_of_service
    )
    if not updated_parking_spot:
        raise HTTPException(status_code=404, detail="Parking spot not found")
    return {
        "user": updated_parking_spot,
        "message": "Parking spot service status updated successfully",
    }


@router.delete("/{parking_spot_id}", dependencies=[Depends(allowed_operations_for_all)])
async def delete_parking_spot_route(
    parking_spot_id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Delete a parking spot by ID.

    This endpoint allows administrators to delete a parking spot by providing its ID.
    Only users with specific permissions (determined by `allowed_operations_for_all`)
    have access to this endpoint.

    Args:
        parking_spot_id (int): The ID of the parking spot to delete.
        session (AsyncSession, optional): The asynchronous session to interact with
            the database. Defaults to Depends(get_session).

    Returns:
        dict: A success message indicating that the parking spot was deleted successfully.

    Raises:
        HTTPException: If the parking spot with the provided ID is not found.
    """
    deleted = await delete_parking_spot(session, parking_spot_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Parking spot not found")
    return {"message": "Parking spot deleted successfully"}


@router.get(
    "",
    response_model=List[ParkingSpotResponse],
    dependencies=[Depends(allowed_operations_for_all)],
)
async def get_all_parking_spots_route(
    session: AsyncSession = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    """
    Retrieve all parking spots.

    This endpoint allows administrators to retrieve all parking spots from the database.
    Only users with specific permissions (determined by `allowed_operations_for_all`)
    have access to this endpoint.

    Args:
        current_user (User, optional): The current user accessing the endpoint. Defaults to
            Depends(auth_service.get_current_user).
        session (AsyncSession, optional): The asynchronous session to interact with
            the database. Defaults to Depends(get_session).
        offset (int, optional): The number of records to offset. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.

    Returns:
        list: A list of dictionaries containing the retrieved parking spots along with
            a success message.

    Raises:
        HTTPException: If there is an error while retrieving parking spots.
    """
    parking_spots = await get_all_parking_spots(session, offset=offset, limit=limit)
    return [
        {"user": parking_spot, "message": "Parking spot retrieved successfully"}
        for parking_spot in parking_spots
    ]
