from dataclasses import dataclass
from .meter import Meter


@dataclass(init=True, repr=True)
class Gas:
    energyType: int
    cui: str
    escalao: int
    status: int
    meter: Meter

    @classmethod
    def from_dict(cls, data):
        return cls(
            energyType=data.get("energyType"),
            cui=data.get("cui"),
            escalao=data.get("escalao"),
            status=data.get("status"),
            meter=Meter.from_dict(data.get("meter"))
        )