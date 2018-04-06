from apistar import Include, Route
from apistar.handlers import docs_urls, static_urls


async def root():
    return {
        'message': 'Welcome to GooBox Nodes API, check /docs for full documentation.'
    }


routes = [
    Route('/', 'GET', root),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]
