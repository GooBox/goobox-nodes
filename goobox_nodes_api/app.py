from apistar import ASyncApp as App
from sqlalchemy import create_engine

from core import sqlalchemy
from goobox_nodes_api.database import Base
from goobox_nodes_api.routes import routes
from goobox_nodes_api.settings import settings

app = App(
    routes=routes,
    components=sqlalchemy.components,
    event_hooks=sqlalchemy.event_hooks,
)

engine = create_engine(settings['DATABASE']['URL'])
Base.metadata.create_all(engine)
