import aiohttp
import pytest

from goobox_nodes import settings
from goobox_nodes.core.components.sia_api_client import SiaAPIClient
from goobox_nodes.core.exceptions import SiaAPIException


class TestCaseSiaNodeResource:
    @pytest.fixture(scope="function")
    def sia_api_client(self):
        return SiaAPIClient()

    @pytest.fixture(scope="function")
    def hosts(self):
        return {
            "hosts": [
                {
                    "recentsuccessfulinteractions": 0,
                    "recentfailedinteractions": 0,
                    "collateral": "string",
                    "uploadbandwidthprice": "string",
                    "publickeystring": "public_key_string",
                    "historicfailedinteractions": 0,
                    "historicdowntime": 0,
                    "ipnets": ["0.0.0.0"],
                    "lasthistoricupdate": 0,
                    "version": "string",
                    "maxcollateral": "string",
                    "maxdownloadbatchsize": 0,
                    "firstseen": 0,
                    "revisionnumber": 0,
                    "sectorsize": 0,
                    "acceptingcontracts": True,
                    "historicuptime": 0,
                    "remainingstorage": 0,
                    "windowsize": 0,
                    "downloadbandwidthprice": "string",
                    "netaddress": "string",
                    "totalstorage": 0,
                    "contractprice": "string",
                    "maxrevisebatchsize": 0,
                    "storageprice": "string",
                    "maxduration": 0,
                    "unlockhash": "string",
                    "historicsuccessfulinteractions": 0,
                    "country": "string",
                    "city": "string",
                }
            ]
        }

    @pytest.fixture(scope="function")
    def processed_hosts(self):
        return [
            {
                "recent_successful_interactions": 0,
                "recent_failed_interactions": 0,
                "collateral": "string",
                "upload_bandwidth_price": "string",
                "public_key_string": "public_key_string",
                "historic_failed_interactions": 0,
                "historic_downtime": 0,
                "ipnets": ["0.0.0.0"],
                "last_historic_update": 0,
                "version": "string",
                "max_collateral": "string",
                "max_download_batch_size": 0,
                "first_seen": 0,
                "revision_number": 0,
                "sector_size": 0,
                "accepting_contracts": True,
                "historic_uptime": 0,
                "remaining_storage": 0,
                "window_size": 0,
                "download_bandwidth_price": "string",
                "net_address": "string",
                "total_storage": 0,
                "contract_price": "string",
                "max_revise_batch_size": 0,
                "storage_price": "string",
                "max_duration": 0,
                "unlock_hash": "string",
                "historic_successful_interactions": 0,
            }
        ]

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_bad_request(self, sia_api_client, responses):
        responses.get("/foo", payload={"foo": "bar"}, headers={"User-Agent": "Sia-Agent"}, status=400)

        with pytest.raises(SiaAPIException) as exc:
            await sia_api_client._request("/foo")

            assert exc.status_code == 400
            assert exc.detail == {"foo": "bar"}

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_server_errror(self, sia_api_client, responses):
        responses.get("/foo", payload={"foo": "bar"}, headers={"User-Agent": "Sia-Agent"}, status=500)

        with pytest.raises(SiaAPIException) as exc:
            await sia_api_client._request("/foo")

            assert exc.status_code == 500
            assert exc.detail is None

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_request_connection_error(self, sia_api_client, responses):
        responses.get(
            "/foo",
            payload={"foo": "bar"},
            headers={"User-Agent": "Sia-Agent"},
            exception=aiohttp.ClientConnectionError(),
        )

        with pytest.raises(SiaAPIException) as exc:
            await sia_api_client._request("/foo")

            assert exc.status_code == 500
            assert exc.detail is None

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_hosts(self, sia_api_client, responses, hosts, processed_hosts):
        responses.get(settings.SIA_API_URL + "/hostdb", payload=hosts, headers={"User-Agent": "Sia-Agent"})

        result = await sia_api_client.hosts()

        assert result == processed_hosts

    @pytest.mark.fast
    @pytest.mark.high
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_active_hosts(self, sia_api_client, responses, hosts, processed_hosts):
        responses.get(settings.SIA_API_URL + "/hostdb/active", payload=hosts, headers={"User-Agent": "Sia-Agent"})

        result = await sia_api_client.active_hosts()

        assert result == processed_hosts
