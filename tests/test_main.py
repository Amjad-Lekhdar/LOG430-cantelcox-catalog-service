from datetime import date

import pytest
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from app.main import catalog_admin_page, health_check
from app.modules.catalog.interfaces.api.router import create_plan, list_plans
from app.modules.catalog.interfaces.api.schemas import CreatePlanRequest


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
