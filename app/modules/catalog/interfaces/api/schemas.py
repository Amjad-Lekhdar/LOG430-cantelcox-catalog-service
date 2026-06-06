from uuid import UUID

from pydantic import BaseModel, Field


class CreatePlanRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=500)
    monthly_price: float = Field(ge=0)
    data_limit_gb: int = Field(ge=0)
    unlimited_calls: bool
    active: bool = True


class UpdatePlanRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=500)
    monthly_price: float = Field(ge=0)
    data_limit_gb: int = Field(ge=0)
    unlimited_calls: bool
    active: bool


class PlanResponse(BaseModel):
    id: UUID
    name: str
    description: str
    monthly_price: float
    data_limit_gb: int
    unlimited_calls: bool
    active: bool
