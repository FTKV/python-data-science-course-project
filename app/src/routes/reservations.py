from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connect_db import get_session
from src.schemas.reservations import ReservationModel, ReservationUpdateModel
from src.database.models import User, Role
from src.repository import reservations
from src.services.roles import RoleAccess
from src.services.auth import auth_service

router = APIRouter(prefix="/reservations", tags=["reservations"])

allowed_operations_for_self = RoleAccess([Role.administrator, Role.user])
allowed_operations_for_all = RoleAccess([Role.administrator])

@router.post("/create", response_model=ReservationModel,
            status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(allowed_operations_for_all)])
async def create_reservation(
    reservation_data: ReservationModel,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new reservation.

    Args:
        reservation_data (ReservationModel): Data for the new reservation.
        session (AsyncSession): Database session.

    Returns:
        ReservationModel: The created reservation.
    """
    return await reservations.create_reservation(reservation_data, session)


@router.get("/{reservation_id}", response_model=ReservationModel,
            dependencies=[Depends(allowed_operations_for_self)])
async def get_reservation(
    reservation_id: UUID4 | int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Get a reservation by its ID.

    Args:
        reservation_id (UUID4 | int): ID of the reservation to retrieve.
        session (AsyncSession): Database session.
        current_user (User): Current user.

    Returns:
        ReservationModel: The retrieved reservation.
    """
    reservation = await reservations.get_reservation_by_id(reservation_id, session)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if not allowed_operations_for_self.has_access(current_user) and reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return reservation


@router.get("", response_model=List[ReservationModel],
            dependencies=[Depends(allowed_operations_for_self)])
async def get_user_reservations(
    offset: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Get reservations for the current user.

    Args:
        offset (int): Offset for pagination.
        limit (int): Limit for pagination.
        session (AsyncSession): Database session.
        current_user (User): Current user.

    Returns:
        List[ReservationModel]: List of reservations for the current user.
    """
    if allowed_operations_for_self.has_access(current_user):
        return await reservations.get_reservations_by_user_id(
            current_user.id, offset, limit, session
        )
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.put("/{reservation_id}", response_model=ReservationModel,
            dependencies=[Depends(allowed_operations_for_all)])
async def update_reservation(
    reservation_id: int,
    reservation_data: ReservationUpdateModel,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Update a reservation.

    Args:
        reservation_id (int): ID of the reservation to update.
        reservation_data (ReservationUpdateModel): Data for updating the reservation.
        session (AsyncSession): Database session.
        current_user (User): Current user.

    Returns:
        ReservationModel: The updated reservation.
    """
    reservation = await reservations.update_reservation(reservation_id, reservation_data, session)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation
