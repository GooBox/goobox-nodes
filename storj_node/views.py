from typing import Dict, List

from apistar import Response
from apistar.backends.sqlalchemy_backend import Session
from apistar.exceptions import NotFound

from storj_node import models, types


async def list_nodes(session: Session) -> List[models.StorjNode]:
    """
    List Storj nodes.
    """
    return [types.StorjNode(node) for node in session.query(models.StorjNode).all()]


async def create_node(session: Session, storj_node: types.StorjNode) -> Response:
    """
    Create a new Storj node.
    """
    node = models.StorjNode(**storj_node)
    session.add(node)
    return Response({'id': node.id}, status=201)


async def retrieve_node(session: Session, node_id: str) -> types.StorjNode:
    """
    Retrieve a Storj node.
    """
    node = session.query(models.StorjNode).get(node_id)
    if node is None:
        raise NotFound

    return types.StorjNode(node)


async def delete_node(session: Session, node_id: str):
    """
    Delete a single Storj node.
    """
    session.query(models.StorjNode).filter(id=node_id).delete()


async def delete_all_nodes(session: Session) -> Dict:
    """
    Delete all Storj nodes.
    """
    num_nodes = session.query(models.StorjNode).count()
    session.query(models.StorjNode).delete()
    return {'deleted': num_nodes}
