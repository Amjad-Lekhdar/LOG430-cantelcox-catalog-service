from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class CreatePlanRequest(BaseModel):
    code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=500)
    monthly_price: float = Field(ge=0)
    data_gb: int = Field(ge=0)
    unlimited_calls: bool
    effective_from: date
    effective_to: date | None = None
    status: str = "ACTIVE"
    active: bool = True


class UpdatePlanRequest(BaseModel):
    code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=120)
    active: bool


class CreatePlanVersionRequest(BaseModel):
    description: str = Field(min_length=1, max_length=500)
    monthly_price: float = Field(ge=0)
    data_gb: int = Field(ge=0)
    unlimited_calls: bool
    effective_from: date
    effective_to: date | None = None
    status: str = "ACTIVE"


class PlanVersionResponse(BaseModel):
    id: UUID
    plan_id: UUID
    version_number: int
    description: str
    monthly_price: float
    data_gb: int
    unlimited_calls: bool
    effective_from: date
    effective_to: date | None
    status: str


class AddonResponse(BaseModel):
    id: UUID
    code: str
    name: str
    description: str
    monthly_price: float
    active: bool
    effective_from: date | None
    effective_to: date | None


class PromotionResponse(BaseModel):
    id: UUID
    name: str
    description: str
    discount_type: str
    discount_value: float
    start_date: date
    end_date: date | None
    active: bool


class PlanResponse(BaseModel):
    id: UUID
    code: str
    name: str
    active_version_id: UUID | None
    active: bool
    active_version: PlanVersionResponse | None = None
    previous_versions: list[PlanVersionResponse] = Field(default_factory=list)
    promotions: list[PromotionResponse] = Field(default_factory=list)
    compatible_addons: list[AddonResponse] = Field(default_factory=list)


class CreatePromotionRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=500)
    discount_type: str = Field(min_length=1, max_length=40)
    discount_value: float = Field(ge=0)
    start_date: date
    end_date: date | None = None
    active: bool = True


class CreateAddonRequest(BaseModel):
    code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=500)
    monthly_price: float = Field(ge=0)
    active: bool = True
    effective_from: date | None = None
    effective_to: date | None = None


class CreateCompatibilityRuleRequest(BaseModel):
    source_product: str = Field(min_length=1, max_length=80)
    target_product: str = Field(min_length=1, max_length=80)
    rule_type: str = Field(min_length=1, max_length=20)


class CompatibilityRuleResponse(BaseModel):
    id: UUID
    source_product: str
    target_product: str
    rule_type: str


class CatalogAuditLogResponse(BaseModel):
    id: UUID
    entity_type: str
    entity_id: UUID
    action: str
    old_value: dict[str, Any] | None
    new_value: dict[str, Any] | None
    performed_by: str
    timestamp: datetime
