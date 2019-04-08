from starlette.background import BackgroundTask
from starlette_api.resources import CRUDListDropResource, resource_method
from starlette_api.responses import APIResponse

from goobox_nodes.core.components.id_generator import IDGenerator
from goobox_nodes.core.components.sia_api_client import SiaAPIClient
from goobox_nodes.nodes import models, schemas
from goobox_nodes.resources import database

__all__ = ["SiaNodeResource"]


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
                200:
                    description:
                        Synchronization request accepted.
        """
        task = BackgroundTask(self._fetch_task, sia_client=sia_client, generator=generator)

        return APIResponse(status_code=202, background=task)

    async def _fetch_task(self, sia_client: SiaAPIClient, generator: IDGenerator):
        # Drop nodes collection
        query = self.model.delete()
        await self.database.execute(query)

        # Insert updated nodes info
        hosts = [
            {
                "id": generator.generate_node_sia(host["public_key_string"]),
                "address": "",  # TODO: Remove when ip geolocation is available
                "country": "",  # TODO: Remove when ip geolocation is available
                "city": "",  # TODO: Remove when ip geolocation is available
                "longitude": 0.0,  # TODO: Remove when ip geolocation is available
                "latitude": 0.0,  # TODO: Remove when ip geolocation is available
                **host,
            }
            for host in await sia_client.active_hosts()
        ]
        query = self.model.insert().values(hosts)
        await self.database.execute(query)
