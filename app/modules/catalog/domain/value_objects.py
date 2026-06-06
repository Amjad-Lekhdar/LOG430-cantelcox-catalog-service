from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "CAD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Plan monthly price must be greater than or equal to 0")
        if self.currency != "CAD":
            raise ValueError("Catalog prices must be expressed in CAD")
