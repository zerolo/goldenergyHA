from dataclasses import dataclass
import datetime

from .electronic_invoice import ElectronicInvoice
from .payment_owner import PaymentOwner
from .last_invoice import LastInvoice
from .direct_debit import DirectDebit
from .billing_address import BillingAddress
from .electricity_product import ElectricityProduct
from .gas_product import GasProduct
from .electricity import Electricity
from .gas import Gas


@dataclass(init=True, repr=True)
class Contract:
    contractNo: str
    initDate: datetime.datetime
    nextReadingDate: datetime.datetime
    alias: str
    paymentOwner: PaymentOwner
    contractOwner: PaymentOwner
    electronicInvoice: ElectronicInvoice
    directDebit: DirectDebit
    electricity: Electricity
    gas: Gas
    billingAddress: BillingAddress
    consumptionPointAddress: BillingAddress
    lastInvoice: LastInvoice
    mgmVoucherCode: str
    balanceAmount: float
    electricityProductList: [ElectricityProduct]
    gasProductList: [GasProduct]

    @classmethod
    def from_dict(cls, data):
        return cls(
            contractNo=data.get("contractNo"),
            initDate=data.get("initDate"),
            nextReadingDate=data.get("nextReadingDate"),
            alias=data.get("alias"),
            paymentOwner=PaymentOwner.from_dict(data.get("paymentOwner")),
            electronicInvoice=ElectronicInvoice.from_dict(data.get("electronicInvoice")),
            contractOwner=PaymentOwner.from_dict(data.get("contractOwner")),
            directDebit=DirectDebit.from_dict(data.get("directDebit")),
            electricity=Electricity.from_dict(data.get("electricity")),
            gas=Gas.from_dict(data.get("gas")),
            billingAddress=BillingAddress.from_dict(data.get("billingAddress")),
            consumptionPointAddress=BillingAddress.from_dict(data.get("consumptionPointAddress")),
            lastInvoice=LastInvoice.from_dict(data.get("lastInvoice")),
            mgmVoucherCode=data.get("mgmVoucherCode"),
            balanceAmount=data.get("balanceAmount"),
            electricityProductList=[
                ElectricityProduct.from_dict(electricity_product) for electricity_product in data.get("electricityProductList")
            ],
            gasProductList=[
                GasProduct.from_dict(gas_product) for gas_product in data.get("gasProductList")
            ]
        )
