from sqlalchemy import Column, Text, Integer, Float, Boolean

from src.db import base, engine


class Pier(base):
    __tablename__ = 'piers'

    id = Column(Integer, primary_key=True)
    
    name = Column(Text)
    lat = Column(Float)
    lng = Column(Float)



base.metadata.create_all(engine)
