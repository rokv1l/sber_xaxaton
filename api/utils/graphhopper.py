import requests

import config


class UnknownError(BaseException):
    pass


def mark_waypoints(coordinates):
    return [{'lng': coords[0], 'lat': coords[1]} for coords in coordinates]


def get_route(points, vehicle='foot'):
    routes = get_routes(points, vehicle)
    return routes[0]


def get_routes(points, vehicle='foot', alternative_routes=None):
    payload = {
        'points': points,
        'points_encoded': False,
        'vehicle': vehicle,
        'instructions': False,  
    }
    
    if alternative_routes:
        payload['ch.disable'] = True
        payload['algorithm'] = 'alternative_route'
        payload['alternative_route.max_paths'] = alternative_routes
        # ниже просто большие параметры, чтобы было больше маршрутов
        payload['alternative_route.max_share_factor'] = 1000
        payload['alternative_route.max_weight_factor'] = 1000
        
    response = requests.post(config.gh_url, json=payload)
    if response.status_code != 200:
        error = response.json()
        raise UnknownError(error['message'])
    
    data = response.json()
    routes = []
    for path in data['paths']:
        route = {
            'waypoints': mark_waypoints(path['points']['coordinates']),
            'dist': int(path['distance']),
            'time': int(path['time']),
        }
        routes.append(route)

    return routes