from uuid import UUID, NAMESPACE_URL, uuid5

from app.modules.catalog.domain.entities import Plan


class PlanRepository:
    def __init__(self) -> None:
        self._plans: dict[UUID, Plan] = {}
        self._seed()

    def add(self, plan: Plan) -> Plan:
        self._plans[plan.id] = plan
        return plan

    def update(self, plan: Plan) -> Plan:
        self._plans[plan.id] = plan
        return plan

    def list(self) -> list[Plan]:
        return list(self._plans.values())

    def get(self, plan_id: UUID) -> Plan | None:
        return self._plans.get(plan_id)

    def get_by_name(self, name: str) -> Plan | None:
        normalized_name = " ".join(name.strip().split()).lower()
        return next(
            (plan for plan in self._plans.values() if plan.name.lower() == normalized_name),
            None,
        )

    def _seed(self) -> None:
        plans = [
            Plan(
                id=uuid5(NAMESPACE_URL, "cantelcox.plan.essential-25"),
                name="Essential 25",
                description="Mobile plan with 25 GB of 5G data and unlimited Canada-wide calls.",
                monthly_price=39.99,
                data_limit_gb=25,
                unlimited_calls=True,
            ),
            Plan(
                id=uuid5(NAMESPACE_URL, "cantelcox.plan.unlimited-100"),
                name="Unlimited 100",
                description="Mobile plan with 100 GB of high-speed data and unlimited calls.",
                monthly_price=59.99,
                data_limit_gb=100,
                unlimited_calls=True,
            ),
            Plan(
                id=uuid5(NAMESPACE_URL, "cantelcox.plan.family-share-200"),
                name="Family Share 200",
                description="Shared family plan with 200 GB of pooled 5G data.",
                monthly_price=94.99,
                data_limit_gb=200,
                unlimited_calls=True,
            ),
        ]
        self._plans = {plan.id: plan for plan in plans}


plan_repository = PlanRepository()
