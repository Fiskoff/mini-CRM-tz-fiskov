from typing import Optional
from random import choices
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    LeadRepository, SourceRepository, DistributionRepository, OperatorRepository, ContactRepository
)
from app.api.schemes.schemas import ContactRegisterRequestSchema, ContactRegisterResponseSchema, OperatorSchema
from core.models import SourceModel, OperatorModel, ContactModel


class LeadDistributionService:
    def __init__(
            self,
            db_session: AsyncSession,
            lead_repo: LeadRepository,
            source_repo: SourceRepository,
            dist_repo: DistributionRepository,
            operator_repo: OperatorRepository,
            contact_repo: ContactRepository
    ):
        self.db_session = db_session
        self.lead_repo = lead_repo
        self.source_repo = source_repo
        self.dist_repo = dist_repo
        self.operator_repo = operator_repo
        self.contact_repo = contact_repo

    async def register_contact(self, request_data: ContactRegisterRequestSchema) -> ContactRegisterResponseSchema:
        lead = await self.lead_repo.find_lead_by_identifier(request_data.lead_identifier)
        if not lead:
            lead = await self.lead_repo.create_lead(request_data.lead_identifier)

        source = await self.source_repo.get_source_by_name(request_data.source_name)
        if not source:
            raise ValueError(f"Источник '{request_data.source_name}' не найдено.")

        assigned_op = await self._assign_operator_to_contact(source)

        contact = await self.contact_repo.create_contact(
            lead_id=lead.id,
            source_id=source.id,
            operator_id=assigned_op.id if assigned_op else None,
            details=request_data.details
        )

        op_schema = OperatorSchema.model_validate(assigned_op) if assigned_op else None
        message = f"Контакт успешно зарегистрирован. {'Назначенный для ' + assigned_op.name if assigned_op else 'Оператор недоступен'}."

        return ContactRegisterResponseSchema(
            contact_id=contact.id,
            lead_id=lead.id,
            source_id=source.id,
            assigned_operator=op_schema,
            message=message
        )

    async def _assign_operator_to_contact(self, source: SourceModel) -> Optional[OperatorModel]:
        dist_settings = await self.dist_repo.get_distribution_settings_for_source(source.id)

        if not dist_settings:
            return None

        eligible_operators_with_weights = []
        for setting in dist_settings:
            op = await self.operator_repo.get_operator(setting.operator_id)
            if not op or not op.is_active:
                continue

            load_query = select(func.count(ContactModel.id)).where(
                ContactModel.operator_id == op.id,
                ContactModel.is_active == True
            )
            load_result = await self.db_session.execute(load_query)
            current_load = load_result.scalar()

            if current_load < op.max_load:
                eligible_operators_with_weights.append((op, float(setting.weight)))

        if not eligible_operators_with_weights:
            return None

        operators, weights = zip(*eligible_operators_with_weights)
        total_weight = sum(weights)
        probabilities = [w / total_weight for w in weights]

        chosen_operator = choices(operators, weights=probabilities, k=1)[0]
        return chosen_operator
