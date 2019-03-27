import asyncio

import pytest
from aioresponses import aioresponses
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.testclient import TestClient

from goobox_nodes import settings
from goobox_nodes.app import app as app_


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """
    Create an instance of the default event loop for each test case.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app():
    url = str(settings.DATABASE_URL)
    assert not database_exists(url), "Test database already exists. Aborting tests."

    try:
        create_database(url)  # Create the test database.
        config = Config("alembic.ini")  # Run the migrations.
        command.upgrade(config, "head")

        yield app_
    finally:
        drop_database(url)  # Drop the test database.


@pytest.fixture
def client(app):
    with TestClient(app) as client_:
        yield client_


@pytest.fixture(scope="class")
def url(app, url_name):
    def get_url(**kwargs):
        result_url = app.url_path_for(url_name, **kwargs)

        return result_url

    return get_url


# Mock for aiohttp requests
@pytest.fixture
def responses():
    with aioresponses() as m:
        yield m
