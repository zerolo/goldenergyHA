from dataclasses import dataclass


@dataclass(init=True, repr=True)
class BillingAddress:
    streetName: str
    number: str
    duplicator: str
    fraction: str
    postCode: str
    city: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            streetName=data.get("streetName"),
            number=data.get("number"),
            duplicator=data.get("duplicator"),
            fraction=data.get("fraction"),
            postCode=data.get("postCode"),
            city=data.get("city")
        )