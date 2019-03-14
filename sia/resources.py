from starlette_api.resources import CRUDListDropResource, resource_method

from core.components.id_generator import IDGenerator
from goobox_nodes_api.resources import database
from sia import models, schemas

__all__ = ["SiaNodeResource"]


class SiaNodeResource(metaclass=CRUDListDropResource):
    name = "sia_node"
    verbose_name = "Sia Node"
    database = database
    model = models.sia_node
    schema = schemas.SiaNode

    @database.transaction()
    @resource_method("/", methods=["POST"])
    async def create(self, element: schemas.SiaNode, generator: IDGenerator):
        return await self._create({"id": generator.generate_sia_node(element["public_key_string"]), **element})
