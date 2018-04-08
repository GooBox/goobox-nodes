import apistar_alembic_migrations
from apistar.backends import sqlalchemy_backend
from apistar.frameworks.asyncio import ASyncIOApp as App

from goobox_nodes_api.routes import routes
from goobox_nodes_api.settings import settings

app = App(
    routes=routes,
    settings=settings,
    commands=apistar_alembic_migrations.commands,  # Install custom commands.
    components=sqlalchemy_backend.components,  # Install custom components.
)
