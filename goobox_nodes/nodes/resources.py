import asyncio
import logging

import aiohttp
from starlette.background import BackgroundTask
from starlette_api.resources import CRUDListDropResource, resource_method
from starlette_api.responses import APIResponse

from goobox_nodes.core.components.id_generator import IDGenerator
from goobox_nodes.core.components.sia_api_client import SiaAPIClient
from goobox_nodes.nodes import models, schemas
from goobox_nodes.resources import database

__all__ = ["SiaNodeResource"]

logger = logging.getLogger(__name__)


class SiaNodeResource(metaclass=CRUDListDropResource):
    name = "sia"
    verbose_name = "Sia Node"
    database = database
    model = models.sia_node
    schema = schemas.SiaNode

    @database.transaction()
    @resource_method("/", methods=["POST"])
    async def create(self, element: schemas.SiaNode, generator: IDGenerator):
        """
            tags:
                - Sia Node
            summary:
                Create a new document.
            description:
                Create a new document in this resource.
            responses:
                201:
                    description:
                        Document created successfully.
        """
        return await self._create({"id": generator.generate_node_sia(element["public_key_string"]), **element})

    @database.transaction()
    @resource_method("/fetch/", methods=["GET"])
    async def fetch(self, sia_client: SiaAPIClient, generator: IDGenerator):
        """
            tags:
                - Sia Node
            summary:
                Fetch nodes info from Sia API.
            description:
                Synchronize Goobox Nodes database with Sia network fetching all nodes info and updating it.
            responses:
                202:
                    description:
                        Synchronization request accepted.
        """
        task = BackgroundTask(self._fetch_task, sia_client=sia_client, generator=generator)

        return APIResponse(status_code=202, background=task)

    async def _fetch_task(self, sia_client: SiaAPIClient, generator: IDGenerator):
        logger.info("Fetching process started")

        # Drop nodes collection
        query = self.model.delete()
        await self.database.execute(query)

        logger.debug("Sia nodes collection dropped")

        # Generate nodes values and calculate id and geolocation
        hosts = []
        sia_hosts = await sia_client.active_hosts()
        logger.debug("Updating %d nodes", len(sia_hosts))
        async with aiohttp.ClientSession() as session:
            for i, host in enumerate(sia_hosts):
                await asyncio.sleep(60 / 150)  # Throttling

                if i % max((len(sia_hosts) // 10), 1) == 0:  # noqa Logging each 10%
                    logger.debug("Nodes updated (%d/%d)", i, len(sia_hosts))

                data = {"id": generator.generate_node_sia(host["public_key_string"]), **host}

                try:
                    address = host["net_address"].split(":")[0]
                    async with session.get(
                        f"http://ip-api.com/json/{address}?fields=country,city,lat,lon,status"
                    ) as response:
                        response.raise_for_status()
                        geolocation = await response.json()

                        if geolocation.get("status", "") != "success":
                            logger.error("Cannot resolve geolocation for address '%s'", address)

                        data.update(
                            {
                                "country": geolocation.get("country"),
                                "city": geolocation.get("city"),
                                "longitude": geolocation.get("lon"),
                                "latitude": geolocation.get("lat"),
                            }
                        )
                except aiohttp.ClientResponseError:
                    logger.error("Error requesting geolocation for address '%s'", address)

                hosts.append(data)

        # Insert updated nodes info
        query = self.model.insert().values(hosts)
        await self.database.execute(query)

        logger.debug("Sia nodes collection updated")
        logger.info("Fetching process finished")
