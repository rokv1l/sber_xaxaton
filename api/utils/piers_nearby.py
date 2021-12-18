from math import radians, cos, sin, asin, sqrt

from src.db import session_maker
from src.pier import Pier
from utils.bikes_nearby import haversine


def get_piers_nearby(lat, lng, radius):
    with session_maker() as session:
        piers = session.query(Pier).all()
        result = []
        for pier in piers:
            length = haversine(lat, lng, pier.lat, pier.lng) * 1000
            if length < radius:
                result.append({
                    'lat': pier.lat,
                    'lng': pier.lng,
                    'lenth': length
                })
    return result
