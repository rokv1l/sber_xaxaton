from copy import deepcopy

import config
from utils.graphhopper import get_route
from utils.multi_modal import enrich_foot_route
from utils.piers_nearby import get_piers_nearby
from utils.river import get_river_route


class UserIsTooFarAway(BaseException):
    pass


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

    route = {
            'waypoints': [route_to_A_pier['waypoints'], river_route, route_from_B_pier['waypoints']],
            'dist': route_to_A_pier['dist'] + len(river_route) * 100 + route_from_B_pier['dist'],
            'time': route_to_A_pier['time'] + len(river_route) * 100 / 3 * 1000 + route_from_B_pier['time'],
            'points': [
                {'lat': A_pier.lat, 'lng': A_pier.lng, 'type': 'pier'},
                {'lat': B_pier.lat, 'lng': B_pier.lng, 'type': 'pier'}
            ]
        }

    routes = [route]
    if _vehicle == 'foot':
        multi_route = enrich_foot_route(deepcopy(route_to_A_pier))
        if multi_route:
            routes.append(multi_route)
    if _vehicle == 'foot':
        multi_route = enrich_foot_route(deepcopy(route_from_B_pier))
        if multi_route:
            routes.append(multi_route)

    routes.append(route)
    return routes


def get_route_to_nearest_pier(point, piers):
    print(point, piers)
    routes = []
    for pier in piers:
        routes.append(
            [
                get_route([f'{point[0]},{point[1]}', f'{pier.lat},{pier.lng}']),
                pier
            ]
        )
    routes = sorted(routes, key= lambda i: i['dist'])
    return routes[0]


def get_route_from_nearest_pier(point, piers):
    print(point, piers)
    routes = []
    for pier in piers:
        routes.append(
            [
                get_route([f'{pier.lat},{pier.lng}', f'{point[0]},{point[1]}']),
                pier
            ]
        )
    routes = sorted(routes, key= lambda i: i['dist'])
    return routes[0]
