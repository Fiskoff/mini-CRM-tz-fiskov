from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ContactModel


class ContactRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_contact(self, lead_id: int, source_id: int, operator_id: Optional[int], details: Optional[str]) -> ContactModel:
        new_contact = ContactModel(
            lead_id=lead_id,
            source_id=source_id,
            operator_id=operator_id,
            details=details,
            is_active=True
        )
        self.db_session.add(new_contact)
        await self.db_session.commit()
        await self.db_session.refresh(new_contact)
        return new_contact
