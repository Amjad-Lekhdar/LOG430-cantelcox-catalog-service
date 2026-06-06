from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.modules.catalog.application.use_cases import (
    CreatePlanUseCase,
    DeactivatePlanUseCase,
    GetPlanUseCase,
    ListPlansUseCase,
    UpdatePlanUseCase,
)
from app.modules.catalog.infrastructure.repositories import plan_repository
from app.modules.catalog.interfaces.api.schemas import (
    CreatePlanRequest,
    PlanResponse,
    UpdatePlanRequest,
)

router = APIRouter(prefix="/v1/catalog", tags=["Catalog"])


@router.post("/plans", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(payload: CreatePlanRequest) -> PlanResponse:
    try:
        plan = CreatePlanUseCase(plan_repository).execute(
            name=payload.name,
            description=payload.description,
            monthly_price=payload.monthly_price,
            data_limit_gb=payload.data_limit_gb,
            unlimited_calls=payload.unlimited_calls,
            active=payload.active,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return PlanResponse(**plan.__dict__)


@router.get("/plans", response_model=list[PlanResponse])
def list_plans(active_only: bool = True) -> list[PlanResponse]:
    plans = ListPlansUseCase(plan_repository).execute(active_only=active_only)
    return [PlanResponse(**plan.__dict__) for plan in plans]


@router.get("/plans/{plan_id}", response_model=PlanResponse)
def get_plan(plan_id: UUID) -> PlanResponse:
    plan = GetPlanUseCase(plan_repository).execute(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return PlanResponse(**plan.__dict__)


@router.put("/plans/{plan_id}", response_model=PlanResponse)
def update_plan(plan_id: UUID, payload: UpdatePlanRequest) -> PlanResponse:
    try:
        plan = UpdatePlanUseCase(plan_repository).execute(
            plan_id=plan_id,
            name=payload.name,
            description=payload.description,
            monthly_price=payload.monthly_price,
            data_limit_gb=payload.data_limit_gb,
            unlimited_calls=payload.unlimited_calls,
            active=payload.active,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return PlanResponse(**plan.__dict__)


@router.delete("/plans/{plan_id}", response_model=PlanResponse)
def deactivate_plan(plan_id: UUID) -> PlanResponse:
    plan = DeactivatePlanUseCase(plan_repository).execute(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return PlanResponse(**plan.__dict__)
