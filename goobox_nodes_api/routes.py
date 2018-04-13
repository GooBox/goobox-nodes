from typing import Dict

from apistar import Include, Route

from storj_node.views import StorjNode


async def root() -> Dict:
    """
    Welcome view.
    """
    return {
        'message': 'Welcome to GooBox Nodes API, check /docs for full documentation.'
    }


routes = [
    Route('/', 'GET', root, name='root'),
    Include('/storj_node', 'storj_node', StorjNode.routes),
]
