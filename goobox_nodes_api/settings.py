import os

from goobox_nodes_api.database import Base

settings = {
    'DATABASE': {
        'URL': f'postgresql://'
               f'{os.environ["DATABASE_USER"]}:{os.environ["DATABASE_PASSWORD"]}'
               f'@{os.environ["DATABASE_HOST"]}:{os.environ["DATABASE_PORT"]}'
               f'/{os.environ["DATABASE_NAME"]}',
        "METADATA": Base.metadata
    }
}
