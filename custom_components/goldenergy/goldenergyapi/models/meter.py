import datetime
from dataclasses import dataclass


@dataclass(init=True, repr=True)
class Meter:
    meterNo: str
    serialNo: str
    initDate: datetime.datetime
    smartMeter: bool

    @classmethod
    def from_dict(cls, data):
        return cls(
            meterNo=data.get("meterNo"),
            serialNo=data.get("serialNo"),
            initDate=data.get("initDate"),
            smartMeter=data.get("smartMeter"),
        )