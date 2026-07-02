from datetime import date
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from app.main import catalog_admin_page, health_check
from app.modules.catalog.domain.services import PlanDomainService
from app.modules.catalog.domain.value_objects import Money
from app.modules.catalog.interfaces.api.router import (
    create_addon,
    create_compatibility_rule,
    create_plan,
    create_plan_version,
    create_promotion,
    deactivate_plan,
    get_plan,
    get_plan_version,
    list_addons,
    list_audit_logs,
    list_compatibility_rules,
    list_plan_versions,
    list_plans,
    list_promotions,
    update_plan,
)
from app.modules.catalog.interfaces.api.schemas import (
    CreateAddonRequest,
    CreateCompatibilityRuleRequest,
    CreatePlanRequest,
    CreatePlanVersionRequest,
    CreatePromotionRequest,
    UpdatePlanRequest,
)


def make_plan_payload(code: str, name: str) -> CreatePlanRequest:
    return CreatePlanRequest(
        code=code,
        name=name,
        description=f"{name} monthly mobile plan.",
        monthly_price=29.99,
        data_gb=15,
        unlimited_calls=True,
        effective_from=date(2026, 2, 1),
    )


def unique_suffix() -> str:
    return uuid4().hex[:8]


def test_health_check_returns_service_status():
    assert health_check() == {
        "status": "ok",
        "service": "catalog-service",
    }


def test_catalog_admin_page_is_served():
    response = catalog_admin_page()

    assert isinstance(response, HTMLResponse)
    assert "CanTelcoX Catalog" in response.body.decode()


def test_list_plans_returns_seed_catalog():
    plans = list_plans()

    assert len(plans) >= 3
    assert {plan.code for plan in plans} >= {
        "ESSENTIAL_25",
        "UNLIMITED_100",
        "FAMILY_SHARE_200",
    }


def test_create_plan_normalizes_input_and_returns_active_version():
    payload = CreatePlanRequest(
        code=" student-15 ",
        name=" Student 15 ",
        description=" Entry mobile plan for students. ",
        monthly_price=29.99,
        data_gb=15,
        unlimited_calls=True,
        effective_from=date(2026, 2, 1),
    )

    plan = create_plan(payload, x_user="pytest")

    assert plan.code == "STUDENT_15"
    assert plan.name == "Student 15"
    assert plan.active is True
    assert plan.active_version is not None
    assert plan.active_version.version_number == 1
    assert plan.active_version.monthly_price == 29.99


def test_create_plan_rejects_duplicate_code():
    payload = CreatePlanRequest(
        code="essential_25",
        name="Another Essential Plan",
        description="A duplicate product code should not be accepted.",
        monthly_price=44.99,
        data_gb=30,
        unlimited_calls=True,
        effective_from=date(2026, 3, 1),
    )

    with pytest.raises(HTTPException) as exc_info:
        create_plan(payload)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "A plan with this product code already exists"


def test_plan_metadata_version_and_deactivation_lifecycle():
    suffix = unique_suffix()
    plan = create_plan(make_plan_payload(f"lifecycle-{suffix}", f"Lifecycle {suffix}"))

    fetched = get_plan(plan.id)
    assert fetched.id == plan.id

    updated = update_plan(
        plan.id,
        UpdatePlanRequest(code=f"lifecycle-{suffix}-new", name=f"Lifecycle Updated {suffix}", active=True),
        x_user="pytest",
    )
    assert updated.code == f"LIFECYCLE_{suffix.upper()}_NEW"
    assert updated.name == f"Lifecycle Updated {suffix}"

    version = create_plan_version(
        plan.id,
        CreatePlanVersionRequest(
            description="Updated lifecycle plan version.",
            monthly_price=34.99,
            data_gb=20,
            unlimited_calls=True,
            effective_from=date(2026, 4, 1),
            status="draft",
        ),
        x_user="pytest",
    )
    assert version.version_number == 2
    assert version.status == "DRAFT"

    versions = list_plan_versions(plan.id)
    assert [plan_version.version_number for plan_version in versions] == [2, 1]
    assert get_plan_version(plan.id, "2").id == version.id

    inactive_plan = deactivate_plan(plan.id, x_user="pytest")
    assert inactive_plan.active is False
    assert inactive_plan.id in {listed_plan.id for listed_plan in list_plans(active_only=False)}


def test_catalog_promotions_addons_compatibility_rules_and_audit_logs():
    suffix = unique_suffix()

    promotion = create_promotion(
        CreatePromotionRequest(
            name=f"Launch Promo {suffix}",
            description="Launch discount for new catalog plans.",
            discount_type="percentage",
            discount_value=10,
            start_date=date(2026, 5, 1),
            active=True,
        ),
        x_user="pytest",
    )
    assert promotion.discount_type == "PERCENTAGE"
    assert promotion.id in {listed_promo.id for listed_promo in list_promotions(active_only=True)}

    addon = create_addon(
        CreateAddonRequest(
            code=f"extra-data-{suffix}",
            name=f"Extra Data {suffix}",
            description="Additional data bucket.",
            monthly_price=12.5,
            effective_from=date(2026, 5, 1),
        ),
        x_user="pytest",
    )
    assert addon.code == f"EXTRA_DATA_{suffix.upper()}"
    assert addon.id in {listed_addon.id for listed_addon in list_addons(active_only=True)}

    rule = create_compatibility_rule(
        CreateCompatibilityRuleRequest(
            source_product="essential-25",
            target_product=addon.code,
            rule_type="optional",
        ),
        x_user="pytest",
    )
    assert rule.rule_type == "OPTIONAL"
    assert rule.id in {listed_rule.id for listed_rule in list_compatibility_rules()}

    addon_logs = list_audit_logs(entity_type="Addon", entity_id=addon.id)
    assert len(addon_logs) == 1
    assert addon_logs[0].performed_by == "pytest"


def test_missing_resources_return_404_errors():
    missing_id = uuid4()

    with pytest.raises(HTTPException) as get_plan_error:
        get_plan(missing_id)
    assert get_plan_error.value.status_code == 404

    with pytest.raises(HTTPException) as update_error:
        update_plan(missing_id, UpdatePlanRequest(code="missing", name="Missing", active=True))
    assert update_error.value.status_code == 404

    with pytest.raises(HTTPException) as deactivate_error:
        deactivate_plan(missing_id)
    assert deactivate_error.value.status_code == 404

    with pytest.raises(HTTPException) as create_version_error:
        create_plan_version(
            missing_id,
            CreatePlanVersionRequest(
                description="Missing plan version.",
                monthly_price=34.99,
                data_gb=20,
                unlimited_calls=True,
                effective_from=date(2026, 4, 1),
            ),
        )
    assert create_version_error.value.status_code == 404

    with pytest.raises(HTTPException) as list_versions_error:
        list_plan_versions(missing_id)
    assert list_versions_error.value.status_code == 404

    with pytest.raises(HTTPException) as get_version_error:
        get_plan_version(missing_id, "1")
    assert get_version_error.value.status_code == 404


def test_domain_validation_errors_are_reported():
    invalid_cases = [
        (PlanDomainService.normalize_code, ("",), "Product code is required"),
        (PlanDomainService.normalize_code, ("bad/code",), "Product code must contain only letters"),
        (PlanDomainService.normalize_name, ("   ",), "Plan name is required"),
        (PlanDomainService.normalize_description, ("   ",), "Plan description is required"),
        (PlanDomainService.ensure_plan_values_are_valid, (10, -1), "Plan data limit"),
        (PlanDomainService.ensure_version_status_is_valid, ("archived",), "Plan version status"),
        (PlanDomainService.ensure_discount_type_is_valid, ("bogus",), "Promotion discount type"),
        (PlanDomainService.ensure_compatibility_rule_type_is_valid, ("linked",), "Compatibility rule type"),
        (Money, (-1,), "Plan monthly price"),
        (Money, (10, "USD"), "Catalog prices must be expressed in CAD"),
    ]

    for function, args, message in invalid_cases:
        with pytest.raises(ValueError, match=message):
            function(*args)
