from dataclasses import dataclass
import datetime


@dataclass(init=True, repr=True)
class DirectDebit:
    activationDate: datetime.datetime
    iban: str
    adc: int
    maximumLimit: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            activationDate=data.get("activationDate"),
            iban=data.get("iban"),
            adc=data.get("adc"),
            maximumLimit=data.get("maximumLimit")
        )