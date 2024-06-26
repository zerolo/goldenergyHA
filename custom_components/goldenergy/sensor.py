from datetime import timedelta
import logging
from typing import Any, Dict

import aiohttp
from .const import (
    DOMAIN,
    PRICE_ENTITY,
    ELECTRICITY_CONSUMPTION_ENTITY,
    GAS_CONSUMPTION_ENTITY,
    DEFAULT_MONETARY_ICON,
    DEFAULT_ELECTRICITY_CONSUMPTION_ICON,
    DEFAULT_GAS_CONSUMPTION_ICON,
    UNIT_OF_MEASUREMENT_EURO,
    UNIT_OF_MEASUREMENT_ELECTRICITY,
    UNIT_OF_MEASUREMENT_GAS,
    ATTRIBUTION,
    CONF_CODE,
    CONF_PASSWORD
)
from goldenergy import Goldenergy

from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity, SensorStateClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

# API Poll time
SCAN_INTERVAL = timedelta(hours=12)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """ Setup Sensors"""
    _LOGGER.debug("Setup Entry")

    session = async_get_clientsession(hass, True)
    api = Goldenergy(session, config_entry.data.get(CONF_CODE), config_entry.data.get(CONF_PASSWORD))
    await api.login()

    sensors = []

    contract = await api.get_active_contract()

    if len(contract.electricityProductList) > 0:
        sensors.append(GoldenergySensor(api, ELECTRICITY_CONSUMPTION_ENTITY))

    if len(contract.gasProductList) > 0:
        sensors.append(GoldenergySensor(api, GAS_CONSUMPTION_ENTITY))

    sensors.append(GoldenergySensor(api, PRICE_ENTITY))

    async_add_entities(sensors, update_before_add=True)


class GoldenergySensor(SensorEntity):
    """ Goldenergy sensor representation """

    def __init__(self, api: Goldenergy, sensorType: str):
        _LOGGER.debug("Init  %s", sensorType)
        super().__init__()
        self._api = api
        self._sensorType = sensorType
        self._invoice = None
        self._electricity_consumption = None
        self._gas_consumption = None
        self._entity_name = self._sensorType
        self._state_class = SensorStateClass.MEASUREMENT
        self._state = None
        self._available = True

        if sensorType == PRICE_ENTITY:
            self._icon = DEFAULT_MONETARY_ICON
            self._unit_of_measurement = UNIT_OF_MEASUREMENT_EURO
            self._device_class = SensorDeviceClass.MONETARY
        elif sensorType == ELECTRICITY_CONSUMPTION_ENTITY:
            self._icon = DEFAULT_ELECTRICITY_CONSUMPTION_ICON
            self._unit_of_measurement = UNIT_OF_MEASUREMENT_ELECTRICITY
            self._device_class = SensorDeviceClass.WATER
            self._state_class = SensorStateClass.TOTAL
        elif sensorType == GAS_CONSUMPTION_ENTITY:
            self._icon = DEFAULT_GAS_CONSUMPTION_ICON
            self._unit_of_measurement = UNIT_OF_MEASUREMENT_GAS
            self._device_class = SensorDeviceClass.GAS
            self._state_class = SensorStateClass.TOTAL

    @property
    def name(self) -> str:
        """ Entity Name """
        return self._entity_name

    @property
    def unique_id(self) -> str:
        """ Sensor unique id """
        return f"{DOMAIN}__{self._entity_name}"

    @property
    def available(self) -> bool:
        return self._available

    @property
    def state(self) -> float:
        return self._state

    @property
    def device_class(self):
        return self._device_class

    @property
    def state_class(self):
        return self._state_class

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def icon(self):
        return self._icon

    @property
    def attribution(self):
        return ATTRIBUTION

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if self._sensorType == PRICE_ENTITY:
            if self._invoice:
                attributes: Dict[str, str] = {
                    "Invoice Number": self._invoice.entryNo,
                    "Customer Number": self._invoice.customerNo,
                    "Contract Number": self._invoice.contractNo,
                    "Due Date": self._invoice.dueDate,
                    "MB Reference": self._invoice.mbReference,
                    "Charged Date": self._invoice.chargedDate,
                    "Billing Method": self._invoice.billingMethodDescription,
                    "Billing Period Init Date": self._invoice.billingPeriodInitDate,
                    "Billing Period End Date": self._invoice.billingPeriodEndDate
                }

                return attributes
        elif self._sensorType == ELECTRICITY_CONSUMPTION_ENTITY:
            if self._electricity_consumption:
                attributes: Dict[str, str] = {
                    "Date": self._electricity_consumption.date,
                    "Meter Number": self._electricity_consumption.meter.meterNo,
                    "Meter Serial Number": self._electricity_consumption.meter.serialNo
                }

                return attributes
        elif self._sensorType == GAS_CONSUMPTION_ENTITY:
            if self._gas_consumption:
                attributes: Dict[str, str] = {
                    "Date": self._gas_consumption.date,
                    "Meter Number": self._gas_consumption.meter.meterNo,
                    "Meter Serial Number": self._gas_consumption.meter.serialNo
                }

                return attributes
        return {}

    async def async_update(self) -> None:
        _LOGGER.debug("Update %s", self._sensorType)
        try:
            await self._api.login()
            if self._sensorType == PRICE_ENTITY:
                self._invoice = await self._api.get_last_invoice()
                _LOGGER.debug("invoice %s", self._invoice)
                if self._invoice:
                    self._state = round(self._invoice.amount, 2)
            elif self._sensorType == ELECTRICITY_CONSUMPTION_ENTITY:
                electricity_consumption = await self._api.get_last_consumption()
                if "ELECTRICITY" in electricity_consumption:
                    self._electricity_consumption = electricity_consumption["ELECTRICITY"]
                    _LOGGER.debug("electricity consumption %s", self._electricity_consumption)
                    if self._electricity_consumption:
                        self._state = round(self._electricity_consumption.realKWh, 2)
            elif self._sensorType == GAS_CONSUMPTION_ENTITY:
                gas_consumption = await self._api.get_last_consumption()
                if "GAS" in gas_consumption:
                    self._gas_consumption = gas_consumption["GAS"]
                    _LOGGER.debug("gas consumption %s", self._gas_consumption)
                    if self._gas_consumption:
                        self._state = round(self._gas_consumption.realM3, 2)
            else:
                self._state = 99
        except aiohttp.ClientError as err:
            self._available = False
            _LOGGER.error("Error retrieving data from Goldenergy API: %s", err)
