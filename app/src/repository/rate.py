from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import Rate as RateModel
from src.schemas.rate import RateCreate, RateUpdate


class RateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_rate_by_id(self, rate_id: int) -> RateModel:
        result = await self.session.execute(select(RateModel).filter(RateModel.id == rate_id))
        return result.scalars().first()

    async def create_rate(self, rate: RateCreate) -> RateModel:
        db_rate = RateModel(**rate.dict())
        self.session.add(db_rate)
        await self.session.commit()
        return db_rate

    async def update_rate(self, rate_id: int, rate_update: RateUpdate) -> RateModel:
        db_rate = await self.get_rate_by_id(rate_id)
        for key, value in rate_update.dict(exclude_unset=True).items():
            setattr(db_rate, key, value)
        await self.session.commit()
        return db_rate

    async def delete_rate(self, rate_id: int) -> None:
        db_rate = await self.get_rate_by_id(rate_id)
        self.session.delete(db_rate)
        await self.session.commit()
