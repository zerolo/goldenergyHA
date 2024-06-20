from dataclasses import dataclass
import datetime


@dataclass(init=True, repr=True)
class GasProduct:
    energyType: int
    escalao: int
    initDate: datetime.datetime
    endDate: datetime.datetime

    @classmethod
    def from_dict(cls, data):
        return cls(
            energyType=data.get("energyType"),
            escalao=data.get("escalao"),
            initDate=data.get("initDate"),
            endDate=data.get("endDate")
        )