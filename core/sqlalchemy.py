import contextlib
import typing

from apistar import http
from apistar.server.components import Component
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from goobox_nodes_api.settings import settings


class SQLAlchemyBackend:
    def __init__(self) -> None:
        """
        Configure a new database backend.

        Args:
          settings: The application settings dictionary.
        """
        database_config = settings['DATABASE']
        url = database_config['URL']
        metadata = database_config['METADATA']

        kwargs = {}
        if url.startswith('postgresql'):  # pragma: nocover
            kwargs['pool_size'] = database_config.get('POOL_SIZE', 5)

        self.metadata = metadata
        self.engine = create_engine(url, **kwargs)
        self.Session = sessionmaker(bind=self.engine)


class SQLAlchemyBackendComponent(Component):
    def resolve(self) -> SQLAlchemyBackend:
        return SQLAlchemyBackend()


class SQLAlchemySessionComponent(Component):
    def resolve(self, backend: SQLAlchemyBackend) -> Session:
        return backend.Session()


class SQLAlchemyTransactionHook:
    def on_response(self, response: http.Response, session: Session) -> http.Response:
        session.commit()
        return response

    def on_error(self, response: http.Response, session: Session) -> http.Response:
        session.rollback()
        return response


components = [
    SQLAlchemyBackendComponent(),
    SQLAlchemySessionComponent(),
]

event_hooks = [
    SQLAlchemyTransactionHook(),
]
