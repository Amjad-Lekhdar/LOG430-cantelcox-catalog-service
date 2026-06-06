from uuid import UUID, uuid4

from app.modules.catalog.domain.entities import Plan
from app.modules.catalog.domain.services import PlanDomainService
from app.modules.catalog.infrastructure.repositories import PlanRepository


class CreatePlanUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(
        self,
        name: str,
        description: str,
        monthly_price: float,
        data_limit_gb: int,
        unlimited_calls: bool,
        active: bool = True,
    ) -> Plan:
        normalized_name = PlanDomainService.normalize_name(name)
        normalized_description = PlanDomainService.normalize_description(description)
        PlanDomainService.ensure_plan_values_are_valid(monthly_price, data_limit_gb)
        PlanDomainService.ensure_plan_can_be_saved(
            self._repository.get_by_name(normalized_name),
            normalized_name,
        )

        plan = Plan(
            id=uuid4(),
            name=normalized_name,
            description=normalized_description,
            monthly_price=monthly_price,
            data_limit_gb=data_limit_gb,
            unlimited_calls=unlimited_calls,
            active=active,
        )
        return self._repository.add(plan)


class ListPlansUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(self, active_only: bool = True) -> list[Plan]:
        plans = self._repository.list()
        if active_only:
            return [plan for plan in plans if plan.active]
        return plans


class GetPlanUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(self, plan_id: UUID) -> Plan | None:
        return self._repository.get(plan_id)


class UpdatePlanUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(
        self,
        plan_id: UUID,
        name: str,
        description: str,
        monthly_price: float,
        data_limit_gb: int,
        unlimited_calls: bool,
        active: bool,
    ) -> Plan | None:
        plan = self._repository.get(plan_id)
        if plan is None:
            return None

        normalized_name = PlanDomainService.normalize_name(name)
        normalized_description = PlanDomainService.normalize_description(description)
        PlanDomainService.ensure_plan_values_are_valid(monthly_price, data_limit_gb)

        existing_plan = self._repository.get_by_name(normalized_name)
        if existing_plan is not None and existing_plan.id != plan_id:
            PlanDomainService.ensure_plan_can_be_saved(existing_plan, normalized_name)

        plan.name = normalized_name
        plan.description = normalized_description
        plan.monthly_price = monthly_price
        plan.data_limit_gb = data_limit_gb
        plan.unlimited_calls = unlimited_calls
        plan.active = active
        return self._repository.update(plan)


class DeactivatePlanUseCase:
    def __init__(self, repository: PlanRepository) -> None:
        self._repository = repository

    def execute(self, plan_id: UUID) -> Plan | None:
        plan = self._repository.get(plan_id)
        if plan is None:
            return None
        plan.active = False
        return self._repository.update(plan)
