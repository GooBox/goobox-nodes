import databases
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


DEBUG = config("DEBUG", cast=bool, default=False)
ENVIRONMENT = config("ENVIRONMENT")
VERSION = config("VERSION", default=None)

SECRET_KEY = config("SECRET_KEY", cast=Secret)

TESTING = config("TESTING", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL", cast=databases.DatabaseURL)

if TESTING:
    DATABASE_URL = DATABASE_URL.replace(database="test_" + DATABASE_URL.database)
