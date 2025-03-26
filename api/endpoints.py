from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from application.dto.request_dto import AnalysisRequestDTO
from application.service.analysis_service import AnalysisService
from infrastructure.di.containers import Container

router = APIRouter(prefix='/api/v1')

@router.post("/analyze")
@inject
async def search(body: AnalysisRequestDTO, analysis_service: AnalysisService = Depends(Provide[Container.analysis_service])):
    return analysis_service.analyze(dto=body)