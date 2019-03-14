from starlette_api.routing import Router

from nodes import resources

__app__ = ["app"]


app = Router()

resources.SiaNodeResource().add_routes(app)
