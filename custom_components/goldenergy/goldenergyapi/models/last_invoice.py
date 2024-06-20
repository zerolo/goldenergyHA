from dataclasses import dataclass
import datetime


@dataclass(init=True, repr=True)
class LastInvoice:
    entryNo: int
    customerNo: str
    contractNo: str
    dueDate: datetime.datetime
    mbReference: str
    charged: bool
    chargedDate: datetime.datetime
    amount: float
    remainingAmount: float
    billingMethodDescription: str
    documentNo: int
    postingDate: datetime.datetime
    billingPeriodInitDate: datetime.datetime
    billingPeriodEndDate: datetime.datetime

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None

        return cls(
            entryNo=data.get("entryNo"),
            customerNo=data.get("customerNo"),
            contractNo=data.get("contractNo"),
            dueDate=data.get("dueDate"),
            mbReference=data.get("mbReference"),
            charged=data.get("charged"),
            chargedDate=data.get("chargedDate"),
            amount=data.get("amount"),
            remainingAmount=data.get("remainingAmount"),
            billingMethodDescription=data.get("billingMethodDescription"),
            documentNo=data.get("documentNo"),
            postingDate=data.get("postingDate"),
            billingPeriodInitDate=data.get("billingPeriodInitDate"),
            billingPeriodEndDate=data.get("billingPeriodEndDate")
        )