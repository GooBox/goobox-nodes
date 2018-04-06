from apistar.frameworks.asyncio import ASyncIOApp as App

from goobox_nodes_api import routes


app = App(routes=routes)
