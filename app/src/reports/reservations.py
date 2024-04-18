"""
Module for reports on reservations.
"""

import csv
from pydantic import UUID4

from fastapi.responses import FileResponse
from sqlalchemy import select, func, and_, case
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import REPORTS_DIR
from src.database.custom_aggregate import add_custom_aggregate
from src.database.models import User, Car, Reservation, Status


async def get_car_checked_out_reservations(
    car_id: UUID4 | int,
    session: AsyncSession,
):
    await add_custom_aggregate(session)
    stmt = (
        select(
            Car.plate,
            case(
                (
                    func.grouping(Reservation.id) == 0,
                    func.first_or_none(Reservation.start_date),
                ),
            ).label("start_date"),
            case(
                (
                    func.grouping(Reservation.id) == 0,
                    func.first_or_none(Reservation.end_date),
                ),
            ).label("end_date"),
            func.sum(Reservation.end_date - Reservation.start_date).label("duration"),
            func.sum(Reservation.debit).label("debit"),
            func.sum(Reservation.credit).label("credit"),
            func.sum((Reservation.debit - Reservation.credit)).label("balance"),
            case(
                (
                    func.grouping(Reservation.id) == 0,
                    func.first_or_none(Reservation.resv_status),
                ),
            ).label("resv_status"),
        )
        .select_from(Reservation)
        .join(Car)
        .filter(
            and_(
                Reservation.car_id == car_id,
                Reservation.resv_status == Status.CHECKED_OUT,
            )
        )
        .order_by("start_date")
        .group_by(Car.plate, func.rollup(Reservation.id))
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
    await add_custom_aggregate(session)
    stmt = (
        select(
            User.username,
            Car.plate,
            case(
                (
                    func.grouping(Reservation.id) == 0,
                    func.first_or_none(Reservation.start_date),
                ),
            ).label("start_date"),
            case(
                (
                    func.grouping(Reservation.id) == 0,
                    func.first_or_none(Reservation.end_date),
                ),
            ).label("end_date"),
            func.sum(Reservation.end_date - Reservation.start_date).label("duration"),
            func.sum(Reservation.debit).label("debit"),
            func.sum(Reservation.credit).label("credit"),
            func.sum((Reservation.debit - Reservation.credit)).label("balance"),
            case(
                (
                    func.grouping(Reservation.id) == 0,
                    func.first_or_none(Reservation.resv_status),
                ),
            ).label("resv_status"),
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
        .group_by(User.username, func.rollup(Car.plate, Reservation.id))
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
