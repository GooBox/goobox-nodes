from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


DEBUG = config.get("DEBUG", cast=bool, default=False)
ENVIRONMENT = config.get("ENVIRONMENT")
VERSION = config.get("VERSION", default=None)

SECRET_KEY = config.get("SECRET_KEY", cast=Secret)

DATABASE_URL = config.get("DATABASE_URL")
