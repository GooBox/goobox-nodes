from starlette_api.applications import Starlette

import nodes.app
from goobox_nodes.components import components
from goobox_nodes.resources import database

app = Starlette(
    components=components,
    title="Goobox Nodes",
    version="1.0.0",
    description="Service that manages the Storage Nodes available for Goobox, collect metadata and keep it updated.",
    schema="/schema/",
    docs="/docs/",
    redoc="/redoc/",
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Root view
@app.route("/", include_in_schema=False)
async def root():
    """
    description: Welcome view.
    responses:
      200:
        description: Welcome message.
    """
    return {
        "message": "Welcome to Goobox Nodes, check /schema/ for API Schema, /docs/ for API docs or /redoc/ for ReDoc."
    }  # noqa


app.mount("/nodes", nodes.app.app, name="nodes")
