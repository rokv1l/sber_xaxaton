from copy import deepcopy

import config
from utils.graphhopper import get_route
from utils.multi_modal import enrich_foot_route
from utils.piers_nearby import get_piers_nearby
from utils.river import get_river_route


class UserIsTooFarAway(BaseException):
    pass

FOOT_COLOR = '#007bff'
SHIP_COLOR = '#000000'


def make_routes_with_water_transport(A, B, _vehicle):
    for i in range(config.lenth_from_pier_limit):
        lng, lat  = A
        A_piers_nearby = get_piers_nearby(lat, lng, i*1000)
        if A_piers_nearby:
            break
    else: 
        # если начальная точка слишком далеко то маршрут не будет построен
        return []
    
    for i in range(config.lenth_from_pier_limit):
        lng, lat = B
        B_piers_nearby = get_piers_nearby(lat, lng, i*1000)
        if B_piers_nearby:
            break
    else:
        # если конечная точка слишком далеко то маршрут не будет построен
        return []  

    route_to_A_pier, A_pier = get_route_to_nearest_pier(A, A_piers_nearby)
    route_from_B_pier, B_pier = get_route_from_nearest_pier(B, B_piers_nearby)
    river_route = get_river_route(A_pier, B_pier)

    print(route_to_A_pier)
    print(route_from_B_pier)
    print(river_route)
    route = {
        'waypoints': [{
            "waypoint": route_to_A_pier["waypoints"],
            "color": FOOT_COLOR,
        },
        {
            "waypoint": [river_route[0], route_to_A_pier["waypoints"][-1]],
            "color": SHIP_COLOR,
        },
        {
            "waypoint": river_route,
            "color": SHIP_COLOR,
        },
        {
            "waypoint": [river_route[-1], route_from_B_pier["waypoints"][0]],
            "color": SHIP_COLOR,
        },
        {
            "waypoint": route_from_B_pier["waypoints"],
            "color": FOOT_COLOR,
        }],
        'dist': route_to_A_pier['dist'] + len(river_route) * 100 + route_from_B_pier['dist'],
        'time': route_to_A_pier['time'] + len(river_route) * 100 / 3 * 1000 + route_from_B_pier['time'],
        'points': [
            {'lat': A_pier['lng'], 'lng': A_pier['lat'], 'type': 'pier'},
            {'lat': B_pier['lng'], 'lng': B_pier['lat'], 'type': 'pier'}
        ]
    }

    routes = [route]

    if _vehicle == 'foot':
        multi_route_A = enrich_foot_route(deepcopy(route_to_A_pier))
    if _vehicle == 'foot':
        multi_route_B = enrich_foot_route(deepcopy(route_from_B_pier))

    if  _vehicle == 'foot' and multi_route_A and multi_route_B:
        route = {
            'waypoints': multi_route_A["waypoints"] + [{
                "waypoint": river_route,
                "color": SHIP_COLOR,
            }] + multi_route_B["waypoints"],
            'dist': multi_route_A['dist'] + len(river_route) * 100 + multi_route_B['dist'],
            'time': multi_route_A['time'] + len(river_route) * 100 / 3 * 1000 + multi_route_B['time'],
            'points': multi_route_A.get("points", []) + multi_route_B.get("points", [])
        }
        routes.append(route)

    return routes


def get_route_to_nearest_pier(point, piers):
    routes = []
    for pier in piers:
        routes.append(
            [
                get_route([point, [pier['lat'], pier['lng']]]),
                pier
            ]
        )
    routes = sorted(routes, key= lambda i: i[0]['dist'])
    return routes[0]


def get_route_from_nearest_pier(point, piers):
    routes = []
    for pier in piers:
        routes.append(
            [
                get_route([[pier['lat'], pier['lng']], point]),
                pier
            ]
        )
    routes = sorted(routes, key= lambda i: i[0]['dist'])
    return routes[0]


def change_lat_lng(waypoints):
    _waypoints = []
    for waypoint in waypoints:
        tmp = {}
        tmp["lat"], tmp["lng"] = waypoint["lng"], waypoint["lat"]
        _waypoints.append(tmp)
    return _waypoints
