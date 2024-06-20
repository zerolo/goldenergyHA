from dataclasses import dataclass
import datetime


@dataclass(init=True, repr=True)
class ElectronicInvoice:
    email: str
    activationDate: datetime.datetime
    active: bool

    @classmethod
    def from_dict(cls, data):
        return cls(
            email=data.get("email"),
            activationDate=data.get("activationDate"),
            active=data.get("active")
        )
