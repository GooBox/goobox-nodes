from apistar_crud.sqlalchemy import Resource
from storj_node import models, types


class StorjNode(metaclass=Resource):
    model = models.StorjNode
    type = types.StorjNode
    methods = ('create', 'retrieve', 'update', 'delete', 'list', 'replace', 'drop')
