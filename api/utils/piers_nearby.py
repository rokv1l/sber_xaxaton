from math import radians, cos, sin, asin, sqrt

from src.db import session_maker
from src.pier import Pier
from utils.bikes_nearby import haversine


def get_piers_nearby(lat, lng, radius):
    result = []
    with session_maker() as session:
        for pier in session.query(Pier).all():
            length = haversine(lat, lng, pier.lat, pier.lng) * 1000
            if length < radius:
                result.append({
                    'lat': pier.lng,
                    'lng': pier.lat,
                    'lenth': length
                })
    return result
