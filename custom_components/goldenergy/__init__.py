import logging

from .goldenergyapi.goldenergy import Goldenergy

from .const import CONF_PASSWORD, CONF_CODE, DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

__version__ = "0.0.9"
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """ Setup component from given entry """
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """ Unload Config Entry """
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """ Reload Config Entry """
    await async_setup_entry(hass, entry)
