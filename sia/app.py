from starlette_api.routing import Router

from sia import resources

__app__ = ["app"]


app = Router()

resources.SiaNodeResource().add_routes(app)
