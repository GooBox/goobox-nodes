from starlette_api.routing import Router

from sia import views

__app__ = ["app"]


app = Router()

app.add_route("/fetch/", views.fetch, name="fetch")
