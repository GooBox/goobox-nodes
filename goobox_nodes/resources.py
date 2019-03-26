import databases
import sqlalchemy

from goobox_nodes import settings

# Database definition.
database_metadata = sqlalchemy.MetaData()

# Use 'force_rollback' during testing, to ensure we do not persist database changes between each test case
database = databases.Database(settings.DATABASE_URL, force_rollback=settings.TESTING)
