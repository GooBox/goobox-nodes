from starlette_api.resources import CRUDListDropResource, resource_method

from core.components.id_generator import IDGenerator
from goobox_nodes.resources import database
from nodes import models, schemas

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
