from app.modules.catalog.domain.entities import Plan
from app.modules.catalog.domain.value_objects import Money


class PlanDomainService:
    VALID_VERSION_STATUSES = {"DRAFT", "ACTIVE", "RETIRED"}
    VALID_DISCOUNT_TYPES = {"AMOUNT", "PERCENTAGE", "FREE_ACTIVATION"}
    VALID_COMPATIBILITY_RULE_TYPES = {"REQUIRES", "EXCLUDES", "OPTIONAL"}

    @staticmethod
    def normalize_code(code: str) -> str:
        normalized_code = "_".join(code.strip().upper().replace("-", "_").split())
        if not normalized_code:
            raise ValueError("Product code is required")
        if not normalized_code.replace("_", "").isalnum():
            raise ValueError("Product code must contain only letters, numbers and underscores")
        return normalized_code

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

    @staticmethod
    def ensure_version_status_is_valid(status: str) -> str:
        normalized_status = status.strip().upper()
        if normalized_status not in PlanDomainService.VALID_VERSION_STATUSES:
            raise ValueError("Plan version status must be DRAFT, ACTIVE or RETIRED")
        return normalized_status

    @staticmethod
    def ensure_discount_type_is_valid(discount_type: str) -> str:
        normalized_type = discount_type.strip().upper()
        if normalized_type not in PlanDomainService.VALID_DISCOUNT_TYPES:
            raise ValueError("Promotion discount type must be AMOUNT, PERCENTAGE or FREE_ACTIVATION")
        return normalized_type

    @staticmethod
    def ensure_compatibility_rule_type_is_valid(rule_type: str) -> str:
        normalized_type = rule_type.strip().upper()
        if normalized_type not in PlanDomainService.VALID_COMPATIBILITY_RULE_TYPES:
            raise ValueError("Compatibility rule type must be REQUIRES, EXCLUDES or OPTIONAL")
        return normalized_type
