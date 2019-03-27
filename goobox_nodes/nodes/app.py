from starlette_api.routing import Router

from goobox_nodes.nodes import resources

__app__ = ["app"]


app = Router()

resources.SiaNodeResource().add_routes(app)
