import typing
import uuid

from goobox_nodes_api import settings
from starlette_api.components import Component


class IDGenerator:
    def __init__(self):
        self._namespaces = {}  # type: typing.Dict[str, uuid.UUID]

    def _get_namespace(self, namespace: str):
        if namespace not in self._namespaces:
            self._namespaces[namespace] = uuid.uuid5(uuid.UUID(str(settings.SECRET_KEY)), namespace)

        return self._namespaces[namespace]

    def generate(self, namespace: str, key: str) -> uuid.UUID:
        return uuid.uuid5(self._get_namespace(namespace), key)

    def generate_node_sia(self, key: str) -> uuid.UUID:
        return self.generate("sia_node", key)


class IDGeneratorComponent(Component):
    def __init__(self):
        self.generator = IDGenerator()

    def resolve(self) -> IDGenerator:
        return self.generator
