from starlette_api.applications import Starlette

import sia.app
from goobox_nodes_api.components import components
from goobox_nodes_api.resources import database

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
@app.route("/")
async def root():
    """
    description: Welcome view.
    responses:
      200:
        description: Welcome message.
    """
    return {
        "message": "Welcome to Goobox Nodes, check /schema/ for API Schema, /docs/ for API docs or /redoc/ for ReDoc."
    }


app.mount("/sia", sia.app.app, name="sia")
