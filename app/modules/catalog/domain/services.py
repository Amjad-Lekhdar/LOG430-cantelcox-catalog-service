from app.modules.catalog.domain.entities import Plan
from app.modules.catalog.domain.value_objects import Money


class PlanDomainService:
    @staticmethod
    def normalize_name(name: str) -> str:
        normalized_name = " ".join(name.strip().split())
        if not normalized_name:
            raise ValueError("Plan name is required")
        return normalized_name

    @staticmethod
    def normalize_description(description: str) -> str:
        normalized_description = " ".join(description.strip().split())
        if not normalized_description:
            raise ValueError("Plan description is required")
        return normalized_description

    @staticmethod
    def ensure_plan_can_be_saved(existing_plan: Plan | None, name: str) -> None:
        if existing_plan is not None and existing_plan.name.lower() == name.lower():
            raise ValueError("A plan with this name already exists")

    @staticmethod
    def ensure_plan_values_are_valid(monthly_price: float, data_limit_gb: int) -> None:
        Money(monthly_price)
        if data_limit_gb < 0:
            raise ValueError("Plan data limit must be greater than or equal to 0")
