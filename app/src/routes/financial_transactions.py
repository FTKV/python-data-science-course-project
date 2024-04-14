"""
Module of users' routes
"""

from pydantic import UUID4
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from redis.asyncio.client import Redis
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connect_db import get_session, get_redis_db1
from src.database.models import User, Role
from src.repository import cars as repository_cars
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.roles import RoleAccess
from src.schemas.financial_transactions import FinancialTransactionModel


router = APIRouter(prefix="/fin_trans", tags=["fin_trans"])

allowed_operations_for_self = RoleAccess([Role.administrator, Role.user])
allowed_operations_for_all = RoleAccess([Role.administrator])


@router.post("/make", status_code=status.HTTP_201_CREATED)
async def create_financial_transactions(
    body: FinancialTransactionModel,
    current_user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_session),
    cache: Redis = Depends(get_redis_db1),
):
    print(body)
