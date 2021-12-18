from sqlalchemy import Column, Text, Integer, Float, Boolean

from src.db import base, engine


class Pier(base):
    __tablename__ = 'piers'

    id = Column(Integer, primary_key=True)

    lat = Column(Float)
    lng = Column(Float)

    is_open = Column(Boolean, default=True)


base.metadata.create_all(engine)
