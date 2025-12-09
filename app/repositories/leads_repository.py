from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import LeadModel, ContactModel


class LeadRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def find_lead_by_identifier(self, identifier: str) -> LeadModel | None:
        query = select(LeadModel).where(
            (LeadModel.external_id == identifier) |
            (LeadModel.phone == identifier) |
            (LeadModel.email == identifier)
        )
        result = await self.db_session.execute(query)
        lead = result.scalar_one_or_none()
        return lead

    async def create_lead(self, external_id: str) -> LeadModel:
        new_lead = LeadModel(external_id=external_id)
        self.db_session.add(new_lead)
        await self.db_session.commit()
        await self.db_session.refresh(new_lead)
        return new_lead

    async def get_leads_with_contacts(self) -> List[LeadModel]:
        from sqlalchemy.orm import selectinload
        query = select(LeadModel).options(
            selectinload(LeadModel.contacts).selectinload(ContactModel.source),
            selectinload(LeadModel.contacts).selectinload(ContactModel.assigned_operator)
        )
        result = await self.db_session.execute(query)
        leads = result.unique().scalars().all()
        return leads
