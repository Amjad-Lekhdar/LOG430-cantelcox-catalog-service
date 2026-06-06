from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PlanModel(Base):
    __tablename__ = "catalog_plans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    monthly_price: Mapped[float] = mapped_column(Float, nullable=False)
    data_limit_gb: Mapped[int] = mapped_column(Integer, nullable=False)
    unlimited_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
