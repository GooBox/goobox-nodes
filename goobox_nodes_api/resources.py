import databases
import sqlalchemy

from goobox_nodes_api import settings


# Database definition.
database_metadata = sqlalchemy.MetaData()
database = databases.Database(settings.DATABASE_URL)
