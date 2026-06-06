from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PlanModel(Base):
    __tablename__ = "catalog_plans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    active_version_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class PlanVersionModel(Base):
    __tablename__ = "catalog_plan_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    plan_id: Mapped[str] = mapped_column(ForeignKey("catalog_plans.id"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    monthly_price: Mapped[float] = mapped_column(Float, nullable=False)
    data_gb: Mapped[int] = mapped_column(Integer, nullable=False)
    unlimited_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")


class PromotionModel(Base):
    __tablename__ = "catalog_promotions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    discount_type: Mapped[str] = mapped_column(String(40), nullable=False)
    discount_value: Mapped[float] = mapped_column(Float, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class AddonModel(Base):
    __tablename__ = "catalog_addons"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    monthly_price: Mapped[float] = mapped_column(Float, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    effective_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)


class CompatibilityRuleModel(Base):
    __tablename__ = "catalog_compatibility_rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    source_product: Mapped[str] = mapped_column(String(80), nullable=False)
    target_product: Mapped[str] = mapped_column(String(80), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(20), nullable=False)


class CatalogAuditLogModel(Base):
    __tablename__ = "catalog_audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    old_value: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    new_value: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    performed_by: Mapped[str] = mapped_column(String(120), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
