import logging
from typing import List, Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.dependencies import get_source_repository
from app.repositories import SourceRepository
from app.api.schemes.schemas import SourceSchema, SourceCreateSchema


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sources", tags=["sources"])

@router.get("/", response_model=List[SourceSchema])
async def get_sources(
    source_repo: Annotated[SourceRepository, Depends(get_source_repository)]
) -> List[SourceSchema]:
    logger.info(f"GET /sources")
    sources = await source_repo.get_sources()
    return sources

@router.post("/", response_model=SourceSchema)
async def create_source(
    new_source_data: SourceCreateSchema,
    source_repo: Annotated[SourceRepository, Depends(get_source_repository)]
) -> SourceSchema:
    logger.info(f"POST /sources")
    new_source = await source_repo.create_source(new_source_data)
    return new_source
