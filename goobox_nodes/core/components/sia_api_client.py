import logging
import typing
from urllib.parse import urlsplit

import aiohttp
import marshmallow
from marshmallow.fields import Boolean, Integer, List, String
from starlette_api.components import Component

from goobox_nodes import settings
from goobox_nodes.core import exceptions

logger = logging.getLogger(__name__)


class SiaNode(marshmallow.Schema):
    accepting_contracts = Boolean(data_key="acceptingcontracts")
    max_download_batch_size = Integer(data_key="maxdownloadbatchsize")
    max_duration = Integer(data_key="maxduration")
    max_revise_batch_size = Integer(data_key="maxrevisebatchsize")
    net_address = String(data_key="netaddress")
    remaining_storage = Integer(data_key="remainingstorage")
    sector_size = Integer(data_key="sectorsize")
    total_storage = Integer(data_key="totalstorage")
    unlock_hash = String(data_key="unlockhash")
    window_size = Integer(data_key="windowsize")
    collateral = String(data_key="collateral")
    max_collateral = String(data_key="maxcollateral")
    contract_price = String(data_key="contractprice")
    download_bandwidth_price = String(data_key="downloadbandwidthprice")
    storage_price = String(data_key="storageprice")
    upload_bandwidth_price = String(data_key="uploadbandwidthprice")
    revision_number = Integer(data_key="revisionnumber")
    version = String(data_key="version")
    first_seen = Integer(data_key="firstseen")
    historic_downtime = Integer(data_key="historicdowntime")
    historic_uptime = Integer(data_key="historicuptime")
    historic_failed_interactions = Integer(data_key="historicfailedinteractions")
    historic_successful_interactions = Integer(data_key="historicsuccessfulinteractions")
    recent_failed_interactions = Integer(data_key="recentfailedinteractions")
    recent_successful_interactions = Integer(data_key="recentsuccessfulinteractions")
    last_historic_update = Integer(data_key="lasthistoricupdate")
    public_key_string = String(data_key="publickeystring")
    ipnets = List(String(), data_key="ipnets")


class URL:
    URL = urlsplit(settings.SIA_API_URL)

    @classmethod
    def hosts(cls) -> str:
        return cls.URL._replace(path="/hostdb").geturl()

    @classmethod
    def active_hosts(cls) -> str:
        return cls.URL._replace(path="/hostdb/active").geturl()


class SiaAPIClient:
    async def _request(
        self, url: str, headers: typing.Optional[typing.Dict[str, str]] = None, *args, **kwargs
    ) -> typing.Dict:
        if headers is None:
            headers = {}

        if "User-Agent" not in headers:
            headers["User-Agent"] = "Sia-Agent"

        try:
            async with aiohttp.ClientSession() as session:
                # Request first page
                logger.debug("Request to '%s' with args '%s' and kwargs '%s'", url, str(args), str(kwargs))
                async with session.get(url, headers=headers, *args, **kwargs) as response:
                    body = await response.json()

                    response.raise_for_status()
                    logger.debug("Response from '%s': %s", url, str(body))
        except aiohttp.ClientResponseError as e:
            if 400 <= e.status < 500:
                logger.debug("4xx - Bad response: %s", str(body))
                raise exceptions.SiaAPIException(status_code=e.status, detail=str(body))
            else:
                logger.debug("5xx - Server error")
                raise exceptions.SiaAPIException(status_code=e.status)
        except aiohttp.ClientConnectionError:
            logger.debug("Client connection error")
            raise exceptions.SiaAPIException(status_code=500, detail="Client connection error")

        return body

    async def _hosts(self, url: str) -> typing.AsyncGenerator[typing.Dict[str, typing.Any], None]:
        response = await self._request(url)

        schema = SiaNode(many=True)
        for host in schema.load(response["hosts"], unknown=marshmallow.EXCLUDE):
            yield host

    async def hosts(self) -> typing.List[typing.Dict[str, typing.Any]]:
        return [i async for i in self._hosts(url=URL.hosts())]

    async def active_hosts(self) -> typing.List[typing.Dict[str, typing.Any]]:
        return [i async for i in self._hosts(url=URL.active_hosts())]


class SiaAPIClientComponent(Component):
    async def resolve(self) -> SiaAPIClient:
        return SiaAPIClient()
