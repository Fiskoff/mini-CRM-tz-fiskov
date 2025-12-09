from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func

from core.models import OperatorModel, ContactModel
from app.api.schemes.schemas import OperatorCreateSchema, OperatorUpdateSchema


class OperatorRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_operators(self) -> List[OperatorModel]:
        query = select(OperatorModel)
        result = await self.db_session.execute(query)
        operators = result.scalars().all()
        return operators

    async def get_operator(self, operator_id: int) -> OperatorModel | None:
        query = select(OperatorModel).where(OperatorModel.id == operator_id)
        result = await self.db_session.execute(query)
        operator = result.scalar_one_or_none()
        return operator

    async def create_operator(self, operator_data: OperatorCreateSchema) -> OperatorModel:
        new_operator = OperatorModel(**operator_data.model_dump())
        self.db_session.add(new_operator)
        await self.db_session.commit()
        await self.db_session.refresh(new_operator)
        return new_operator

    async def update_operator(self, operator_id: int, operator_update: OperatorUpdateSchema) -> OperatorModel | None:
        stmt = (
            update(OperatorModel)
            .where(OperatorModel.id == operator_id)
            .values(**operator_update.model_dump(exclude_unset=True))
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

        updated_operator = await self.get_operator(operator_id)
        return updated_operator

    async def get_active_operators_with_load(self, operator_ids: List[int]) -> List[OperatorModel]:
        query = select(OperatorModel).where(
            OperatorModel.id.in_(operator_ids),
            OperatorModel.is_active == True
        )
        result = await self.db_session.execute(query)
        operators = result.scalars().all()

        operators_with_load = []
        for op in operators:
            load_query = select(func.count(ContactModel.id)).where(
                ContactModel.operator_id == op.id,
                ContactModel.is_active == True
            )
            load_result = await self.db_session.execute(load_query)
            current_load = load_result.scalar()
            op.current_load = current_load
            operators_with_load.append(op)
        return operators_with_load
