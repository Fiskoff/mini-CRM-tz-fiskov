from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import SourceOperatorDistributionModel
from app.api.schemes.schemas import DistributionSettingCreateSchema


class DistributionRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_distribution_settings_for_source(self, source_id: int) -> List[SourceOperatorDistributionModel]:
        query = select(SourceOperatorDistributionModel).where(SourceOperatorDistributionModel.source_id == source_id)
        result = await self.db_session.execute(query)
        settings = result.scalars().all()
        return settings

    async def create_or_update_distribution_setting(self, setting_data: DistributionSettingCreateSchema) -> SourceOperatorDistributionModel: # Уточнен тип аргумента и возврата
        existing_setting_query = select(SourceOperatorDistributionModel).where(
            SourceOperatorDistributionModel.source_id == setting_data.source_id,
            SourceOperatorDistributionModel.operator_id == setting_data.operator_id
        )
        existing_result = await self.db_session.execute(existing_setting_query)
        existing_setting = existing_result.scalar_one_or_none()

        if existing_setting:
            existing_setting.weight = setting_data.weight
            await self.db_session.commit()
            await self.db_session.refresh(existing_setting)
            return existing_setting
        else:
            new_setting = SourceOperatorDistributionModel(**setting_data.model_dump())
            self.db_session.add(new_setting)
            await self.db_session.commit()
            await self.db_session.refresh(new_setting)
            return new_setting

    async def get_operator_ids_for_source(self, source_id: int) -> List[int]:
        query = select(SourceOperatorDistributionModel.operator_id).where(
            SourceOperatorDistributionModel.source_id == source_id
        )
        result = await self.db_session.execute(query)
        operator_ids = [row[0] for row in result.fetchall()]
        return operator_ids
