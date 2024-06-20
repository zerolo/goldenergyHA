import logging
from .const import *

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class Connection:

    def __init__(self, session,):
        self._websession = session
        self._token = None

    def set_token(self, token):
        self._token = token

    def __get_auth_headers(self):
        _LOGGER.debug("Goldenergy API AuthHeaders")
        headers = {**DEFAULT_HEADERS}
        if self._token is not None:
            headers[AUTH_HEADER] = AUTH_TOKEN_PREFIX + self._token
        return headers

    async def api_request(self, url: str, method="get", data=None, params=None):
        async with getattr(self._websession, method)(url, headers=self.__get_auth_headers(), json=data,
                                                     params=params) as response:
            try:
                if response.status == 200 and response.content_type == JSON_CONTENT:
                    return await response.json()
                else:
                    raise Exception("HTTP Request Error: %s", str(response.status) + " " + str(response.content_type))
            except Exception as err:
                _LOGGER.error("API request error: %s", err)
                return None
