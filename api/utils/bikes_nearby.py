from math import radians, cos, sin, asin, sqrt

from src.db import session_maker
from src.bike_base import BikeBase


def haversine(lat1, lng1, lat2, lng2):
    R = 6371.0  # this is in km

    dLat = radians(lat2 - lat1)
    dLng = radians(lng2 - lng1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLng / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c


def get_bike_bases_nearby(lat, lng, radius):
    result = []
    with session_maker() as session:
        for base in session.query(BikeBase).all():
            length = haversine(lat, lng, base.lat, base.lng) * 1000
            if length < radius and base.is_open:
                result.append({
                    'address': base.address,
                    'lat': base.lat,
                    'lng': base.lng,
                    'is_open': base.is_open,
                    'lenth': length
                })
    return result
