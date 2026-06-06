from datetime import date
from uuid import UUID, uuid4

from app.modules.catalog.domain.entities import (
    Addon,
    CompatibilityRule,
    Plan,
    PlanVersion,
    Promotion,
)
from app.modules.catalog.domain.services import PlanDomainService
from app.modules.catalog.infrastructure.repositories import PlanRepository


class CreatePlanUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(
        self,
        code: str,
        name: str,
        description: str,
        monthly_price: float,
        data_gb: int,
        unlimited_calls: bool,
        effective_from: date,
        effective_to: date | None,
        status: str,
        active: bool = True,
        performed_by: str = "system",
    ) -> Plan:
        normalized_code = PlanDomainService.normalize_code(code)
        normalized_name = PlanDomainService.normalize_name(name)
        normalized_description = PlanDomainService.normalize_description(description)
        PlanDomainService.ensure_plan_values_are_valid(monthly_price, data_gb)
        normalized_status = PlanDomainService.ensure_version_status_is_valid(status)
        PlanDomainService.ensure_plan_can_be_saved(
            self._repository.get_plan_by_name(normalized_name),
            normalized_name,
        )
        if self._repository.get_plan_by_code(normalized_code) is not None:
            raise ValueError("A plan with this product code already exists")

        plan = Plan(id=uuid4(), code=normalized_code, name=normalized_name, active=active)
        version = PlanVersion(
            id=uuid4(),
            plan_id=plan.id,
            version_number=1,
            description=normalized_description,
            monthly_price=monthly_price,
            data_gb=data_gb,
            unlimited_calls=unlimited_calls,
            effective_from=effective_from,
            effective_to=effective_to,
            status=normalized_status,
        )
        return self._repository.add_plan(plan, version, performed_by)


class ListPlansUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(self, active_only: bool = True) -> list[Plan]:
        plans = self._repository.list_plans()
        if active_only:
            return [plan for plan in plans if plan.active]
        return plans


class GetPlanUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(self, plan_id: UUID) -> Plan | None:
        return self._repository.get_plan(plan_id)


class UpdatePlanMetadataUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(
        self,
        plan_id: UUID,
        code: str,
        name: str,
        active: bool,
        performed_by: str,
    ) -> Plan | None:
        plan = self._repository.get_plan(plan_id)
        if plan is None:
            return None

        normalized_code = PlanDomainService.normalize_code(code)
        normalized_name = PlanDomainService.normalize_name(name)
        existing_plan = self._repository.get_plan_by_name(normalized_name)
        if existing_plan is not None and existing_plan.id != plan_id:
            PlanDomainService.ensure_plan_can_be_saved(existing_plan, normalized_name)
        existing_code = self._repository.get_plan_by_code(normalized_code)
        if existing_code is not None and existing_code.id != plan_id:
            raise ValueError("A plan with this product code already exists")

        old_value = self._repository.plan_to_dict(plan)
        plan.code = normalized_code
        plan.name = normalized_name
        plan.active = active
        return self._repository.update_plan_metadata(plan, performed_by, old_value)


class CreatePlanVersionUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(
        self,
        plan_id: UUID,
        description: str,
        monthly_price: float,
        data_gb: int,
        unlimited_calls: bool,
        effective_from: date,
        effective_to: date | None,
        status: str,
        performed_by: str,
    ) -> PlanVersion | None:
        plan = self._repository.get_plan(plan_id)
        if plan is None:
            return None
        PlanDomainService.ensure_plan_values_are_valid(monthly_price, data_gb)
        normalized_description = PlanDomainService.normalize_description(description)
        normalized_status = PlanDomainService.ensure_version_status_is_valid(status)
        version = PlanVersion(
            id=uuid4(),
            plan_id=plan_id,
            version_number=self._repository.next_version_number(plan_id),
            description=normalized_description,
            monthly_price=monthly_price,
            data_gb=data_gb,
            unlimited_calls=unlimited_calls,
            effective_from=effective_from,
            effective_to=effective_to,
            status=normalized_status,
        )
        return self._repository.add_plan_version(version, performed_by)


class ListPlanVersionsUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(self, plan_id: UUID) -> list[PlanVersion] | None:
        if self._repository.get_plan(plan_id) is None:
            return None
        return self._repository.list_versions(plan_id)


class GetPlanVersionUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(self, plan_id: UUID, version: str) -> PlanVersion | None:
        if self._repository.get_plan(plan_id) is None:
            return None
        return self._repository.get_version(plan_id, version)


class DeactivatePlanUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(self, plan_id: UUID, performed_by: str) -> Plan | None:
        plan = self._repository.get_plan(plan_id)
        if plan is None:
            return None
        old_value = self._repository.plan_to_dict(plan)
        plan.active = False
        return self._repository.update_plan_metadata(plan, performed_by, old_value)


class CreatePromotionUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(
        self,
        name: str,
        description: str,
        discount_type: str,
        discount_value: float,
        start_date: date,
        end_date: date | None,
        active: bool,
        performed_by: str,
    ) -> Promotion:
        normalized_type = PlanDomainService.ensure_discount_type_is_valid(discount_type)
        promotion = Promotion(
            id=uuid4(),
            name=PlanDomainService.normalize_name(name),
            description=PlanDomainService.normalize_description(description),
            discount_type=normalized_type,
            discount_value=discount_value,
            start_date=start_date,
            end_date=end_date,
            active=active,
        )
        return self._repository.add_promotion(promotion, performed_by)


class CreateAddonUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(
        self,
        code: str,
        name: str,
        description: str,
        monthly_price: float,
        active: bool,
        effective_from: date | None,
        effective_to: date | None,
        performed_by: str,
    ) -> Addon:
        normalized_code = PlanDomainService.normalize_code(code)
        if self._repository.get_addon_by_code(normalized_code) is not None:
            raise ValueError("An addon with this product code already exists")
        PlanDomainService.ensure_plan_values_are_valid(monthly_price, 0)
        addon = Addon(
            id=uuid4(),
            code=normalized_code,
            name=PlanDomainService.normalize_name(name),
            description=PlanDomainService.normalize_description(description),
            monthly_price=monthly_price,
            active=active,
            effective_from=effective_from,
            effective_to=effective_to,
        )
        return self._repository.add_addon(addon, performed_by)


class CreateCompatibilityRuleUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(
        self,
        source_product: str,
        target_product: str,
        rule_type: str,
        performed_by: str,
    ) -> CompatibilityRule:
        rule = CompatibilityRule(
            id=uuid4(),
            source_product=PlanDomainService.normalize_code(source_product),
            target_product=PlanDomainService.normalize_code(target_product),
            rule_type=PlanDomainService.ensure_compatibility_rule_type_is_valid(rule_type),
        )
        return self._repository.add_compatibility_rule(rule, performed_by)
