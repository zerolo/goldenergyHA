from dataclasses import dataclass


@dataclass(init=True, repr=True)
class PaymentOwner:
    customerNo: str
    name: str
    nif: int
    phone: str
    mobile: str
    email: str
    isLastPaymentOwner: bool

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None

        return cls(
            customerNo=data.get("customerNo"),
            name=data.get("name"),
            nif=data.get("nif"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            email=data.get("email"),
            isLastPaymentOwner=data.get("isLastPaymentOwner")
        )