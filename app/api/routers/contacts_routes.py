import logging
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException


from app.api.dependencies.dependencies import get_lead_distribution_service, get_lead_repository
from app.services.lead_distribution_service import LeadDistributionService
from app.repositories import LeadRepository
from app.api.schemes.schemas import (
    ContactRegisterRequestSchema, ContactRegisterResponseSchema, LeadWithContactsSchema, ContactViewSchema
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/register", response_model=ContactRegisterResponseSchema)
async def register_contact(
        contact_request: ContactRegisterRequestSchema,
        distribution_service: Annotated[LeadDistributionService, Depends(get_lead_distribution_service)]
):
    logger.info(f"POST /contacts/register")
    try:
        result = await distribution_service.register_contact(contact_request)
        return result
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        logger.error(f"Ошибка при регистрации контакта: {error}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера при регистрации.")


@router.get("/state", response_model=List[LeadWithContactsSchema])
async def view_state(lead_repo: Annotated[LeadRepository, Depends(get_lead_repository)]):
    logger.info(f"POST /contacts/state")
    leads = await lead_repo.get_leads_with_contacts()

    results = []
    for lead in leads:
        contact_views = []
        for contact in lead.contacts:
            contact_view = ContactViewSchema(
                id=contact.id,
                source_name=contact.source.name,
                operator_name=contact.assigned_operator.name if contact.assigned_operator else None,
                created_at=contact.created_at,
                is_active=contact.is_active,
                details=contact.details
            )
            contact_views.append(contact_view)

        lead_with_contacts = LeadWithContactsSchema.model_validate(lead)
        lead_with_contacts.contacts = contact_views
        results.append(lead_with_contacts)

    return results
