from starlette_api.exceptions import HTTPException


class SiaAPIException(HTTPException):
    pass


class InitializationError(Exception):
    pass
