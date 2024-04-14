from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import RateDetail as RateDetailModel
from src.schemas.rate_detail import RateDetailInput, RateDetailUpdate


class RateDetailRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_rate_detail_by_id(self, rate_detail_id: int) -> RateDetailModel:
        result = await self.session.execute(select(RateDetailModel).filter(RateDetailModel.id == rate_detail_id))
        return result.scalars().first()

    async def create_rate_detail(self, rate_detail: RateDetailInput) -> RateDetailModel:
        db_rate_detail = RateDetailModel(**rate_detail.dict())
        self.session.add(db_rate_detail)
        await self.session.commit()
        return db_rate_detail

    async def update_rate_detail(self, rate_detail_id: int, rate_detail_update: RateDetailUpdate) -> RateDetailModel:
        db_rate_detail = await self.get_rate_detail_by_id(rate_detail_id)
        for key, value in rate_detail_update.dict(exclude_unset=True).items():
            setattr(db_rate_detail, key, value)
        await self.session.commit()
        return db_rate_detail

    async def delete_rate_detail(self, rate_detail_id: int) -> None:
        db_rate_detail = await self.get_rate_detail_by_id(rate_detail_id)
        self.session.delete(db_rate_detail)
        await self.session.commit()
