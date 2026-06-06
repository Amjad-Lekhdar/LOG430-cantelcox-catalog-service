from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID


@dataclass
class Plan:
    id: UUID
    code: str
    name: str
    active_version_id: UUID | None = None
    active: bool = field(default=True)


@dataclass
class PlanVersion:
    id: UUID
    plan_id: UUID
    version_number: int
    description: str
    monthly_price: float
    data_gb: int
    unlimited_calls: bool
    effective_from: date
    effective_to: date | None = None
    status: str = "ACTIVE"


@dataclass
class Promotion:
    id: UUID
    name: str
    description: str
    discount_type: str
    discount_value: float
    start_date: date
    end_date: date | None = None
    active: bool = True


@dataclass
class Addon:
    id: UUID
    code: str
    name: str
    description: str
    monthly_price: float
    active: bool = True
    effective_from: date | None = None
    effective_to: date | None = None


@dataclass
class CompatibilityRule:
    id: UUID
    source_product: str
    target_product: str
    rule_type: str


@dataclass
class CatalogAuditLog:
    id: UUID
    entity_type: str
    entity_id: UUID
    action: str
    old_value: dict | None
    new_value: dict | None
    performed_by: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
