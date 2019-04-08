import databases
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


# Environment
DEBUG = config("DEBUG", cast=bool, default=False)
ENVIRONMENT = config("ENVIRONMENT")
VERSION = config("VERSION", default=None)

# Application
SECRET_KEY = config("SECRET_KEY", cast=Secret)

# Database
DATABASE_URL = config("DATABASE_URL", cast=databases.DatabaseURL)

# Sia
SIA_API_URL = config("SIA_API_URL")

# Testing
TESTING = config("TESTING", cast=bool, default=False)
if TESTING:
    DATABASE_URL = DATABASE_URL.replace(database="test_" + DATABASE_URL.database)
