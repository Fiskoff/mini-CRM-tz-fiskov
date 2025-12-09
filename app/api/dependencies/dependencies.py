from typing import AsyncGenerator
from fastapi import Depends

from core.db_config import get_async_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    LeadRepository, SourceRepository, DistributionRepository, OperatorRepository, ContactRepository
)
from app.services.lead_distribution_service import LeadDistributionService


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_async_db_session() as session:
        yield session

async def get_operator_repository(
    db_session: AsyncSession = Depends(get_db_session)
) -> OperatorRepository:
    return OperatorRepository(db_session)

async def get_source_repository(
    db_session: AsyncSession = Depends(get_db_session)
) -> SourceRepository:
    return SourceRepository(db_session)

async def get_distribution_repository(
    db_session: AsyncSession = Depends(get_db_session)
) -> DistributionRepository:
    return DistributionRepository(db_session)

async def get_lead_repository(
    db_session: AsyncSession = Depends(get_db_session)
) -> LeadRepository:
    return LeadRepository(db_session)

async def get_contact_repository(
    db_session: AsyncSession = Depends(get_db_session)
) -> ContactRepository:
    return ContactRepository(db_session)

async def get_lead_distribution_service(
    db_session: AsyncSession = Depends(get_db_session),
    lead_repo: LeadRepository = Depends(get_lead_repository),
    source_repo: SourceRepository = Depends(get_source_repository),
    dist_repo: DistributionRepository = Depends(get_distribution_repository),
    operator_repo: OperatorRepository = Depends(get_operator_repository),
    contact_repo: ContactRepository = Depends(get_contact_repository)
) -> LeadDistributionService:
    return LeadDistributionService(
        db_session=db_session,
        lead_repo=lead_repo,
        source_repo=source_repo,
        dist_repo=dist_repo,
        operator_repo=operator_repo,
        contact_repo=contact_repo
    )
