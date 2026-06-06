from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class Plan:
    id: UUID
    name: str
    description: str
    monthly_price: float
    data_limit_gb: int
    unlimited_calls: bool
    active: bool = field(default=True)
