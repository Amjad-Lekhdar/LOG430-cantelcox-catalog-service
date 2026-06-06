from dataclasses import asdict
from datetime import date
from uuid import UUID, NAMESPACE_URL, uuid4, uuid5

from app.modules.catalog.domain.entities import (
    Addon,
    CatalogAuditLog,
    CompatibilityRule,
    Plan,
    PlanVersion,
    Promotion,
)


class PlanRepository:
    def __init__(self) -> None:
        self._plans: dict[UUID, Plan] = {}
        self._versions: dict[UUID, PlanVersion] = {}
        self._promotions: dict[UUID, Promotion] = {}
        self._addons: dict[UUID, Addon] = {}
        self._compatibility_rules: dict[UUID, CompatibilityRule] = {}
        self._audit_logs: list[CatalogAuditLog] = []
        self._seed()

    def add_plan(self, plan: Plan, version: PlanVersion, performed_by: str) -> Plan:
        self._plans[plan.id] = plan
        self._versions[version.id] = version
        plan.active_version_id = version.id
        self.add_audit_log("Plan", plan.id, "CREATE", None, self.plan_to_dict(plan), performed_by)
        self.add_audit_log(
            "PlanVersion",
            version.id,
            "CREATE",
            None,
            self.version_to_dict(version),
            performed_by,
        )
        return plan

    def update_plan_metadata(self, plan: Plan, performed_by: str, old_value: dict) -> Plan:
        self._plans[plan.id] = plan
        self.add_audit_log("Plan", plan.id, "UPDATE", old_value, self.plan_to_dict(plan), performed_by)
        return plan

    def add_plan_version(self, version: PlanVersion, performed_by: str) -> PlanVersion:
        plan = self._plans[version.plan_id]
        old_plan = self.plan_to_dict(plan)
        self._versions[version.id] = version
        plan.active_version_id = version.id
        self.add_audit_log(
            "PlanVersion",
            version.id,
            "CREATE",
            None,
            self.version_to_dict(version),
            performed_by,
        )
        self.add_audit_log("Plan", plan.id, "SET_ACTIVE_VERSION", old_plan, self.plan_to_dict(plan), performed_by)
        return version

    def list_plans(self) -> list[Plan]:
        return list(self._plans.values())

    def get_plan(self, plan_id: UUID) -> Plan | None:
        return self._plans.get(plan_id)

    def get_plan_by_name(self, name: str) -> Plan | None:
        normalized_name = " ".join(name.strip().split()).lower()
        return next(
            (plan for plan in self._plans.values() if plan.name.lower() == normalized_name),
            None,
        )

    def get_plan_by_code(self, code: str) -> Plan | None:
        normalized_code = code.strip().upper()
        return next((plan for plan in self._plans.values() if plan.code == normalized_code), None)

    def get_active_version(self, plan: Plan) -> PlanVersion | None:
        if plan.active_version_id is None:
            return None
        return self._versions.get(plan.active_version_id)

    def get_version(self, plan_id: UUID, version_id_or_number: str) -> PlanVersion | None:
        versions = self.list_versions(plan_id)
        for version in versions:
            if str(version.id) == version_id_or_number or str(version.version_number) == version_id_or_number:
                return version
        return None

    def list_versions(self, plan_id: UUID) -> list[PlanVersion]:
        return sorted(
            [version for version in self._versions.values() if version.plan_id == plan_id],
            key=lambda version: version.version_number,
            reverse=True,
        )

    def next_version_number(self, plan_id: UUID) -> int:
        versions = self.list_versions(plan_id)
        if not versions:
            return 1
        return max(version.version_number for version in versions) + 1

    def add_promotion(self, promotion: Promotion, performed_by: str) -> Promotion:
        self._promotions[promotion.id] = promotion
        self.add_audit_log(
            "Promotion",
            promotion.id,
            "CREATE",
            None,
            asdict(promotion),
            performed_by,
        )
        return promotion

    def list_promotions(self, active_only: bool = False) -> list[Promotion]:
        promotions = list(self._promotions.values())
        if active_only:
            promotions = [promotion for promotion in promotions if promotion.active]
        return sorted(promotions, key=lambda promotion: promotion.start_date)

    def add_addon(self, addon: Addon, performed_by: str) -> Addon:
        self._addons[addon.id] = addon
        self.add_audit_log("Addon", addon.id, "CREATE", None, asdict(addon), performed_by)
        return addon

    def list_addons(self, active_only: bool = False) -> list[Addon]:
        addons = list(self._addons.values())
        if active_only:
            addons = [addon for addon in addons if addon.active]
        return sorted(addons, key=lambda addon: addon.code)

    def get_addon_by_code(self, code: str) -> Addon | None:
        normalized_code = code.strip().upper()
        return next((addon for addon in self._addons.values() if addon.code == normalized_code), None)

    def add_compatibility_rule(self, rule: CompatibilityRule, performed_by: str) -> CompatibilityRule:
        self._compatibility_rules[rule.id] = rule
        self.add_audit_log("CompatibilityRule", rule.id, "CREATE", None, asdict(rule), performed_by)
        return rule

    def list_compatibility_rules(self) -> list[CompatibilityRule]:
        return list(self._compatibility_rules.values())

    def list_compatible_addons_for_plan(self, plan_code: str) -> list[Addon]:
        excluded_codes = {
            rule.target_product
            for rule in self._compatibility_rules.values()
            if rule.source_product == plan_code and rule.rule_type == "EXCLUDES"
        }
        compatible_codes = {
            rule.target_product
            for rule in self._compatibility_rules.values()
            if rule.source_product == plan_code and rule.rule_type in {"OPTIONAL", "REQUIRES"}
        }
        addons = self.list_addons(active_only=True)
        if compatible_codes:
            addons = [addon for addon in addons if addon.code in compatible_codes]
        return [addon for addon in addons if addon.code not in excluded_codes]

    def list_audit_logs(self, entity_type: str | None = None, entity_id: UUID | None = None) -> list[CatalogAuditLog]:
        logs = self._audit_logs
        if entity_type is not None:
            logs = [log for log in logs if log.entity_type == entity_type]
        if entity_id is not None:
            logs = [log for log in logs if log.entity_id == entity_id]
        return sorted(logs, key=lambda log: log.timestamp, reverse=True)

    def add_audit_log(
        self,
        entity_type: str,
        entity_id: UUID,
        action: str,
        old_value: dict | None,
        new_value: dict | None,
        performed_by: str,
    ) -> CatalogAuditLog:
        log = CatalogAuditLog(
            id=uuid4(),
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            old_value=old_value,
            new_value=new_value,
            performed_by=performed_by,
        )
        self._audit_logs.append(log)
        return log

    def plan_to_dict(self, plan: Plan) -> dict:
        return asdict(plan)

    def version_to_dict(self, version: PlanVersion) -> dict:
        return asdict(version)

    def _seed(self) -> None:
        seed_date = date(2026, 1, 1)
        seed_plans = [
            (
                "essential-25",
                "ESSENTIAL_25",
                "Essential 25",
                "Mobile plan with 25 GB of 5G data and unlimited Canada-wide calls.",
                39.99,
                25,
            ),
            (
                "unlimited-100",
                "UNLIMITED_100",
                "Unlimited 100",
                "Mobile plan with 100 GB of high-speed data and unlimited calls.",
                59.99,
                100,
            ),
            (
                "family-share-200",
                "FAMILY_SHARE_200",
                "Family Share 200",
                "Shared family plan with 200 GB of pooled 5G data.",
                94.99,
                200,
            ),
        ]
        for slug, code, name, description, price, data_gb in seed_plans:
            plan = Plan(
                id=uuid5(NAMESPACE_URL, f"cantelcox.plan.{slug}"),
                code=code,
                name=name,
            )
            version = PlanVersion(
                id=uuid5(NAMESPACE_URL, f"cantelcox.plan-version.{slug}.1"),
                plan_id=plan.id,
                version_number=1,
                description=description,
                monthly_price=price,
                data_gb=data_gb,
                unlimited_calls=True,
                effective_from=seed_date,
            )
            plan.active_version_id = version.id
            self._plans[plan.id] = plan
            self._versions[version.id] = version

        self._addons = {
            addon.id: addon
            for addon in [
                Addon(
                    id=uuid5(NAMESPACE_URL, "cantelcox.addon.usa-roaming"),
                    code="USA_ROAMING",
                    name="Roaming USA",
                    description="Daily roaming access for calls, text and data in the United States.",
                    monthly_price=12.0,
                    effective_from=seed_date,
                ),
                Addon(
                    id=uuid5(NAMESPACE_URL, "cantelcox.addon.extra-data-20"),
                    code="EXTRA_DATA_20",
                    name="Donnees supplementaires 20 GB",
                    description="Additional 20 GB data bucket for compatible mobile plans.",
                    monthly_price=15.0,
                    effective_from=seed_date,
                ),
                Addon(
                    id=uuid5(NAMESPACE_URL, "cantelcox.addon.device-protection"),
                    code="DEVICE_PROTECTION",
                    name="Protection appareil",
                    description="Device protection with repair and replacement support.",
                    monthly_price=9.99,
                    effective_from=seed_date,
                ),
            ]
        }

        promotion = Promotion(
            id=uuid5(NAMESPACE_URL, "cantelcox.promotion.black-friday"),
            name="Black Friday",
            description="20 dollars de rabais pendant 6 mois sur les plans admissibles.",
            discount_type="AMOUNT",
            discount_value=20.0,
            start_date=date(2026, 11, 1),
            end_date=date(2026, 11, 30),
        )
        self._promotions[promotion.id] = promotion


plan_repository = PlanRepository()
