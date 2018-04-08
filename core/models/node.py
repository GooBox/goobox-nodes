from sqlalchemy import Column, Float, String

__all__ = ['NodeMixin']


class NodeMixin:
    address = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
