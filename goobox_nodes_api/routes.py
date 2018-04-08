from typing import Dict

from apistar import Include, Route, annotate
from apistar.handlers import docs_urls, static_urls

import storj_node.routes


@annotate(authentication=None, permissions=None, exclude_from_schema=True)
async def root() -> Dict:
    """
    Welcome view.
    """
    return {
        'message': 'Welcome to GooBox Nodes API, check /docs for full documentation.'
    }


routes = [
    Route('/', 'GET', root),
    Include('/docs', docs_urls),
    Include('/static', static_urls),
    Include('/storj_node', storj_node.routes.routes, namespace='storj_node'),
]
