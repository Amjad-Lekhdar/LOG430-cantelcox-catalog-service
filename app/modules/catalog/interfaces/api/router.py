from dataclasses import asdict
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException, status

from app.modules.catalog.application.use_cases import (
    CreateAddonUseCase,
    CreateCompatibilityRuleUseCase,
    CreatePlanUseCase,
    CreatePlanVersionUseCase,
    CreatePromotionUseCase,
    DeactivatePlanUseCase,
    GetPlanUseCase,
    GetPlanVersionUseCase,
    ListPlansUseCase,
    ListPlanVersionsUseCase,
    UpdatePlanMetadataUseCase,
)
from app.modules.catalog.domain.entities import Plan
from app.modules.catalog.infrastructure.repositories import plan_repository
from app.modules.catalog.interfaces.api.schemas import (
    AddonResponse,
    CatalogAuditLogResponse,
    CompatibilityRuleResponse,
    CreateAddonRequest,
    CreateCompatibilityRuleRequest,
    CreatePlanRequest,
    CreatePlanVersionRequest,
    CreatePromotionRequest,
    PlanResponse,
    PlanVersionResponse,
    PromotionResponse,
    UpdatePlanRequest,
)

router = APIRouter(prefix="/v1/catalog", tags=["Catalog"])


def _performed_by(x_user: str | None) -> str:
    return x_user or "catalog-admin"


def _version_response(version) -> PlanVersionResponse:
    return PlanVersionResponse(**asdict(version))


def _promotion_response(promotion) -> PromotionResponse:
    return PromotionResponse(**asdict(promotion))


def _addon_response(addon) -> AddonResponse:
    return AddonResponse(**asdict(addon))


def _plan_response(plan: Plan) -> PlanResponse:
    active_version = plan_repository.get_active_version(plan)
    previous_versions = [
        version
        for version in plan_repository.list_versions(plan.id)
        if version.id != plan.active_version_id
    ]
    return PlanResponse(
        id=plan.id,
        code=plan.code,
        name=plan.name,
        active_version_id=plan.active_version_id,
        active=plan.active,
        active_version=_version_response(active_version) if active_version is not None else None,
        previous_versions=[_version_response(version) for version in previous_versions],
        promotions=[_promotion_response(promotion) for promotion in plan_repository.list_promotions(active_only=True)],
        compatible_addons=[
            _addon_response(addon) for addon in plan_repository.list_compatible_addons_for_plan(plan.code)
        ],
    )


@router.post("/plans", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(payload: CreatePlanRequest, x_user: str | None = Header(default=None)) -> PlanResponse:
    try:
        plan = CreatePlanUseCase(plan_repository).execute(
            code=payload.code,
            name=payload.name,
            description=payload.description,
            monthly_price=payload.monthly_price,
            data_gb=payload.data_gb,
            unlimited_calls=payload.unlimited_calls,
            effective_from=payload.effective_from,
            effective_to=payload.effective_to,
            status=payload.status,
            active=payload.active,
            performed_by=_performed_by(x_user),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _plan_response(plan)


@router.get("/plans", response_model=list[PlanResponse])
def list_plans(active_only: bool = True) -> list[PlanResponse]:
    plans = ListPlansUseCase(plan_repository).execute(active_only=active_only)
    return [_plan_response(plan) for plan in plans]


@router.get("/plans/{plan_id}", response_model=PlanResponse)
def get_plan(plan_id: UUID) -> PlanResponse:
    plan = GetPlanUseCase(plan_repository).execute(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return _plan_response(plan)


@router.put("/plans/{plan_id}", response_model=PlanResponse)
def update_plan(plan_id: UUID, payload: UpdatePlanRequest, x_user: str | None = Header(default=None)) -> PlanResponse:
    try:
        plan = UpdatePlanMetadataUseCase(plan_repository).execute(
            plan_id=plan_id,
            code=payload.code,
            name=payload.name,
            active=payload.active,
            performed_by=_performed_by(x_user),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return _plan_response(plan)


@router.delete("/plans/{plan_id}", response_model=PlanResponse)
def deactivate_plan(plan_id: UUID, x_user: str | None = Header(default=None)) -> PlanResponse:
    plan = DeactivatePlanUseCase(plan_repository).execute(plan_id, performed_by=_performed_by(x_user))
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return _plan_response(plan)


@router.post("/plans/{plan_id}/versions", response_model=PlanVersionResponse, status_code=status.HTTP_201_CREATED)
def create_plan_version(
    plan_id: UUID,
    payload: CreatePlanVersionRequest,
    x_user: str | None = Header(default=None),
) -> PlanVersionResponse:
    try:
        version = CreatePlanVersionUseCase(plan_repository).execute(
            plan_id=plan_id,
            description=payload.description,
            monthly_price=payload.monthly_price,
            data_gb=payload.data_gb,
            unlimited_calls=payload.unlimited_calls,
            effective_from=payload.effective_from,
            effective_to=payload.effective_to,
            status=payload.status,
            performed_by=_performed_by(x_user),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if version is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return _version_response(version)


@router.get("/plans/{plan_id}/versions", response_model=list[PlanVersionResponse])
def list_plan_versions(plan_id: UUID) -> list[PlanVersionResponse]:
    versions = ListPlanVersionsUseCase(plan_repository).execute(plan_id)
    if versions is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return [_version_response(version) for version in versions]


@router.get("/plans/{plan_id}/versions/{version}", response_model=PlanVersionResponse)
def get_plan_version(plan_id: UUID, version: str) -> PlanVersionResponse:
    plan_version = GetPlanVersionUseCase(plan_repository).execute(plan_id, version)
    if plan_version is None:
        raise HTTPException(status_code=404, detail="Plan version not found")
    return _version_response(plan_version)


@router.post("/promotions", response_model=PromotionResponse, status_code=status.HTTP_201_CREATED)
def create_promotion(
    payload: CreatePromotionRequest,
    x_user: str | None = Header(default=None),
) -> PromotionResponse:
    try:
        promotion = CreatePromotionUseCase(plan_repository).execute(
            name=payload.name,
            description=payload.description,
            discount_type=payload.discount_type,
            discount_value=payload.discount_value,
            start_date=payload.start_date,
            end_date=payload.end_date,
            active=payload.active,
            performed_by=_performed_by(x_user),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _promotion_response(promotion)


@router.get("/promotions", response_model=list[PromotionResponse])
def list_promotions(active_only: bool = False) -> list[PromotionResponse]:
    return [
        _promotion_response(promotion)
        for promotion in plan_repository.list_promotions(active_only=active_only)
    ]


@router.post("/addons", response_model=AddonResponse, status_code=status.HTTP_201_CREATED)
def create_addon(payload: CreateAddonRequest, x_user: str | None = Header(default=None)) -> AddonResponse:
    try:
        addon = CreateAddonUseCase(plan_repository).execute(
            code=payload.code,
            name=payload.name,
            description=payload.description,
            monthly_price=payload.monthly_price,
            active=payload.active,
            effective_from=payload.effective_from,
            effective_to=payload.effective_to,
            performed_by=_performed_by(x_user),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _addon_response(addon)


@router.get("/addons", response_model=list[AddonResponse])
def list_addons(active_only: bool = False) -> list[AddonResponse]:
    return [_addon_response(addon) for addon in plan_repository.list_addons(active_only=active_only)]


@router.post("/compatibility-rules", response_model=CompatibilityRuleResponse, status_code=status.HTTP_201_CREATED)
def create_compatibility_rule(
    payload: CreateCompatibilityRuleRequest,
    x_user: str | None = Header(default=None),
) -> CompatibilityRuleResponse:
    try:
        rule = CreateCompatibilityRuleUseCase(plan_repository).execute(
            source_product=payload.source_product,
            target_product=payload.target_product,
            rule_type=payload.rule_type,
            performed_by=_performed_by(x_user),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CompatibilityRuleResponse(**asdict(rule))


@router.get("/compatibility-rules", response_model=list[CompatibilityRuleResponse])
def list_compatibility_rules() -> list[CompatibilityRuleResponse]:
    return [
        CompatibilityRuleResponse(**asdict(rule))
        for rule in plan_repository.list_compatibility_rules()
    ]


@router.get("/audit-logs", response_model=list[CatalogAuditLogResponse])
def list_audit_logs(entity_type: str | None = None, entity_id: UUID | None = None) -> list[CatalogAuditLogResponse]:
    return [
        CatalogAuditLogResponse(**asdict(log))
        for log in plan_repository.list_audit_logs(entity_type=entity_type, entity_id=entity_id)
    ]
