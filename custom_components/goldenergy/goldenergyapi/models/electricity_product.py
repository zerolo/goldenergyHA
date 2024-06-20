from dataclasses import dataclass
import datetime


@dataclass(init=True, repr=True)
class ElectricityProduct:
    energyType: int
    power: str
    initDate: datetime.datetime
    endDate: datetime.datetime

    @classmethod
    def from_dict(cls, data):
        return cls(
            energyType=data.get("energyType"),
            power=data.get("power"),
            initDate=data.get("initDate"),
            endDate=data.get("endDate")
        )