from apistar import Route

from storj_node.views import create_node, delete_all_nodes, delete_node, list_nodes, retrieve_node

routes = [
    Route('/', 'GET', list_nodes, name='list'),
    Route('/', 'POST', create_node, name='create'),
    Route('/', 'DELETE', delete_all_nodes, name='delete_all'),
    Route('/{node_id}/', 'GET', retrieve_node, name='retrieve'),
    Route('/{node_id}/', 'DELETE', delete_node, name='delete'),
]
