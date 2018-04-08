from sqlalchemy import Column, DateTime, Float, Integer, String

from core.models.node import NodeMixin
from goobox_nodes_api.database import Base

__all__ = ['StorjNode']


class StorjNode(NodeMixin, Base):
    __tablename__ = "storj_node"

    id = Column(String, primary_key=True)
    last_seen = Column(DateTime)
    last_timeout = Column(DateTime)
    port = Column(Integer, nullable=False)
    protocol = Column(String)
    reputation = Column(Integer, nullable=False)
    response_time = Column(Float, nullable=False)
    space_available = Column(Integer, nullable=False)
    timeout_rate = Column(Integer, nullable=False)
    user_agent = Column(String)

    def __repr__(self):
        return f'<StorjNode(id={self.id})>'
