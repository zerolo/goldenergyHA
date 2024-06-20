import logging

from .connection import Connection
from .const import *
from .models import Contract, Consumption, LastInvoice

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class Goldenergy:
    def __init__(self, session, code, password):
        self._connection = Connection(session)
        self._contract: Contract = None
        self._last_consumption = None
        self._code = code
        self._password = password

    async def login(self):
        _LOGGER.debug("Goldenergy API Login")
        url = ENDPOINT + LOGIN_PATH

        data = {
            CODE_PARAM: self._code,
            PWD_PARAM: self._password
        }

        res = await self._connection.api_request(url, method="post", data=data)
        if res is not None:
            try:
                self._connection.set_token(res["result"]["token"])
                return True
            except:
                return False
        return False

    async def get_contract(self, contract_number: str) -> Contract:
        _LOGGER.debug("Goldenergy API Contract")

        url = ENDPOINT + CONTRACT_PATH

        contract_api_response = await self._connection.api_request(url, params={"ContractNo": contract_number})
        contract = contract_api_response["result"]

        self._contract = Contract.from_dict(contract)
        return self._contract

    async def get_active_contract(self) -> Contract:
        _LOGGER.debug("Goldenergy API Contract")

        url = ENDPOINT + CONTRACT_LIST_PATH

        contracts_api_response = await self._connection.api_request(url)
        contracts = contracts_api_response["result"]

        if len(contracts["contracts"]) > 1:
            # vai ver o que tem o status = 1
            for contract in contracts["contracts"]:
                if contract["status"] == 1:
                    self._contract = Contract.from_dict(contract)
                    break

        elif len(contracts["contracts"]) == 1:
            self._contract = Contract.from_dict(contracts["contracts"][0])

        return self._contract

    async def get_last_invoice(self, contract_number: str = None) -> LastInvoice:
        _LOGGER.debug("Goldenergy API Contract")

        if contract_number is None:
            await self.get_active_contract()
            contract_number = self._contract.contractNo

        url = ENDPOINT + CONTRACT_PATH

        contract_api_response = await self._connection.api_request(url, params={"ContractNo": contract_number})
        contract = contract_api_response["result"]

        self._contract = Contract.from_dict(contract)
        return self._contract.lastInvoice

    async def get_last_consumption(self, contract_no: str = None):
        _LOGGER.debug("Goldenergy API Consumptions")

        if contract_no is None:
            await self.get_active_contract()
            contract_no = self._contract.contractNo

        url = ENDPOINT + CONSUMPTIONS_PATH

        consumptions_api_response = await self._connection.api_request(
            url,
            params={"ContractNo": contract_no}
        )
        consumption = consumptions_api_response["result"]["items"][0]

        self._last_consumption = Consumption.from_dict(consumption)
        return self._last_consumption
