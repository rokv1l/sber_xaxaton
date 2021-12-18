import json
from .bikes_nearby import haversine


class NoClosePointsError(Exception):
    pass


def get_river():
    with open("/api/utils/moscow_river.json") as f:
        return json.load(f)

    
def get_river_route(pier_from, pier_to):
    river = get_river()

    from_idx, to_idx = None, None
    min_dist_from, min_dist_to = float("inf"), float("inf")
    for i, point in enumerate(river):
        lat, lng = point["coords"]
        dist_from = haversine(pier_from['lng'], pier_from['lat'], lat, lng)
        dist_to = haversine(pier_to['lng'], pier_to['lat'], lat, lng)

        if dist_from < min_dist_from:
            min_dist_from = dist_from
            from_idx = i

        if dist_to < min_dist_to:
            min_dist_to = dist_to
            to_idx = i

    if any([from_idx is None, to_idx is None]):
        raise NoClosePointsError

    if from_idx < to_idx:
        return to_waypoints(river[from_idx:min(to_idx+1, len(river))])
    return to_waypoints(river[from_idx:max(to_idx-1, 0):-1])


def to_waypoints(points):
    return [
        {"lat": point["coords"][0],
         "lng": point["coords"][1]}
        for point in points
    ]
