from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import SourceModel
from app.api.schemes.schemas import SourceCreateSchema


class SourceRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_sources(self) -> List[SourceModel]:
        query = select(SourceModel)
        result = await self.db_session.execute(query)
        sources = result.scalars().all()
        return sources

    async def get_source_by_name(self, name: str) -> SourceModel | None:
        query = select(SourceModel).where(SourceModel.name == name)
        result = await self.db_session.execute(query)
        source = result.scalar_one_or_none()
        return source

    async def get_source(self, source_id: int) -> SourceModel | None:
        query = select(SourceModel).where(SourceModel.id == source_id)
        result = await self.db_session.execute(query)
        source = result.scalar_one_or_none()
        return source

    async def create_source(self, source_data: SourceCreateSchema) -> SourceModel:
        new_source = SourceModel(**source_data.model_dump())
        self.db_session.add(new_source)
        await self.db_session.commit()
        await self.db_session.refresh(new_source)
        return new_source
