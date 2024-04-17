"""
Module for reports on reservations.
"""

import csv
from typing import Union
from pydantic import UUID4

from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from src.conf.config import REPORTS_DIR
from src.database.models import User, Car, Reservation, Status


async def get_car_checked_out_reservations(
    car_id: UUID4 | int,
    session: AsyncSession,
):
    stmt = (
        select(
            Reservation.start_date,
            Reservation.end_date,
            (Reservation.end_date - Reservation.start_date).label("duration"),
            Reservation.debit,
            Reservation.credit,
            (Reservation.debit - Reservation.credit).label("balance"),
            Reservation.resv_status,
        )
        .select_from(Reservation)
        .filter(
            and_(
                Reservation.car_id == car_id,
                Reservation.resv_status == Status.CHECKED_OUT,
            )
        )
        .order_by(Reservation.start_date)
    )
    reservations = await session.execute(stmt)
    rows = reservations.all()
    fields = reservations.keys()
    filename = "report.csv"
    filepath = REPORTS_DIR / filename
    with open(filepath, "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
    return FileResponse(
        filepath,
        media_type="text/csv",
        filename=filename,
        status_code=200,
    )


async def get_user_checked_out_reservations(
    username: str,
    session: AsyncSession,
):
    stmt = (
        select(
            Reservation.start_date,
            Reservation.end_date,
            (Reservation.end_date - Reservation.start_date).label("duration"),
            Reservation.debit,
            Reservation.credit,
            (Reservation.debit - Reservation.credit).label("balance"),
            Reservation.resv_status,
        )
        .select_from(Reservation)
        .join(Car)
        .join(User)
        .filter(
            and_(
                User.username == username,
                Reservation.resv_status == Status.CHECKED_OUT,
            )
        )
        .order_by(Reservation.start_date)
    )
    reservations = await session.execute(stmt)
    rows = reservations.all()
    fields = reservations.keys()
    filename = "report.csv"
    filepath = REPORTS_DIR / filename
    with open(filepath, "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
    return FileResponse(
        filepath,
        media_type="text/csv",
        filename=filename,
        status_code=200,
    )
