import logging
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.dependencies import get_operator_repository
from app.repositories import OperatorRepository
from app.api.schemes.schemas import OperatorSchema, OperatorCreateSchema, OperatorUpdateSchema


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/operators", tags=["operators"])

@router.get("/", response_model=List[OperatorSchema])
async def get_operators(
    operator_repo: Annotated[OperatorRepository, Depends(get_operator_repository)]
) -> List[OperatorSchema]:
    logger.info(f"GET /operators")
    operators = await operator_repo.get_operators()
    return operators

@router.post("/", response_model=OperatorSchema)
async def create_operator(
    new_operator_data: OperatorCreateSchema,
    operator_repo: Annotated[OperatorRepository, Depends(get_operator_repository)]
) -> OperatorSchema:
    logger.info(f"POST /operators")
    new_operator = await operator_repo.create_operator(new_operator_data)
    return new_operator

@router.put("/{operator_id}", response_model=OperatorSchema)
async def update_operator(
    operator_id: int,
    operator_update: OperatorUpdateSchema,
    operator_repo: Annotated[OperatorRepository, Depends(get_operator_repository)]
) -> OperatorSchema:
    logger.info(f"PUT /operators/operator_id")
    updated_op = await operator_repo.update_operator(operator_id, operator_update)
    if not updated_op:
        raise HTTPException(status_code=404, detail="Оператор не найден")
    return updated_op
