from apistar.parsers import JSONParser
from apistar.renderers import JSONRenderer

from goobox_nodes_api.database import Base
from goobox_nodes_api.environment import env

settings = {
    'DATABASE': {
        'URL': f'postgresql://'
               f'{env["DATABASE_USER"]}:{env["DATABASE_PASSWORD"]}'
               f'@{env["DATABASE_HOST"]}:{env["DATABASE_PORT"]}'
               f'/{env["DATABASE_NAME"]}',
        "METADATA": Base.metadata
    },
    'PARSERS': (
        JSONParser(),
    ),
    'RENDERERS': (
        JSONRenderer(),
    ),
}
