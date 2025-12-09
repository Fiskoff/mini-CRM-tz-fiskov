import logging
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.dependencies import get_distribution_repository, get_source_repository, get_operator_repository
from app.repositories import DistributionRepository, SourceRepository, OperatorRepository
from app.api.schemes.schemas import DistributionSettingSchema, DistributionSettingCreateSchema


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/distributions", tags=["distributions"])

@router.get("/source/{source_id}", response_model=List[DistributionSettingSchema])
async def get_distribution_settings(
        source_id: int,
        distribution_repo: Annotated[DistributionRepository, Depends(get_distribution_repository)]
) -> List[DistributionSettingSchema]:
    logger.info(f"GET /distributions/sources/source_id")
    settings = await distribution_repo.get_distribution_settings_for_source(source_id)
    return settings


@router.post("/", response_model=DistributionSettingSchema)
async def create_or_update_distribution(
        setting_data: DistributionSettingCreateSchema,
        distribution_repo: Annotated[DistributionRepository, Depends(get_distribution_repository)],
        source_repo: Annotated[SourceRepository, Depends(get_source_repository)],
        operator_repo: Annotated[OperatorRepository, Depends(get_operator_repository)]
):
    logger.info(f"POST /distributions")
    source = await source_repo.get_source(setting_data.source_id)
    operator = await operator_repo.get_operator(setting_data.operator_id)
    if not source or not operator:
        raise HTTPException(status_code=404, detail="Источник или оператор не найдены.")

    setting = await distribution_repo.create_or_update_distribution_setting(setting_data)
    return setting