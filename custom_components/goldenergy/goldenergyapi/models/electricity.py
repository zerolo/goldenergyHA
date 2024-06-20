from dataclasses import dataclass
from .meter import Meter


@dataclass(init=True, repr=True)
class Electricity:
    energyType: int
    cpe: str
    power: str
    tariffType: int
    selfConsumption: bool
    status: int
    meter: Meter

    @classmethod
    def from_dict(cls, data):
        return cls(
            energyType=data.get("energyType"),
            cpe=data.get("cpe"),
            power=data.get("power"),
            tariffType=data.get("tariffType"),
            selfConsumption=data.get("selfConsumption"),
            status=data.get("status"),
            meter=Meter.from_dict(data.get("meter"))
        )