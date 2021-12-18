from collections import defaultdict
from datetime import datetime

from utils.graphhopper import get_route
from utils.bikes_nearby import get_bike_bases_nearby

FOOT_COLOR = '#A0E720'
BIKE_COLOR = '#00ADEE'

def enrich_foot_route(route):
    transfers = find_transfers_to_bike(route)
    if transfers:
        bike_segment = get_route(
            [transfers['start']['base'], transfers['end']['base']], 
            vehicle='bike'
        )
        segment_1 = get_route([tuple(route['waypoints'][0].values()),  transfers['start']['base']], vehicle="foot")
        segment_2 = get_route([transfers['end']['base'], tuple(route['waypoints'][-1].values())], vehicle="foot")
        route['waypoints'] = [
            {
                "waypoint": segment_1["waypoints"],
                "color": FOOT_COLOR,
            },
            {
                "waypoint": bike_segment['waypoints'],
                "color": BIKE_COLOR,
            },
            {
                "waypoint": segment_2["waypoints"],
                "color": FOOT_COLOR,
            },
        ]
        route['dist'] = bike_segment['dist'] + segment_1['dist'] + segment_2['dist']

        route['time'] = bike_segment['time'] + segment_1['time'] + segment_2['time']

        route['points'] = [
            {'lat': transfers['start']['base'][1], 'lng': transfers['start']['base'][0], 'type': 'bike'},
            {'lat': transfers['end']['base'][1], 'lng': transfers['end']['base'][0], 'type': 'bike'}
        ]

    return route


def find_transfers_to_bike(route):
    total_len = len(route['waypoints'])

    start = int(total_len * 0.17)
    start_point_idx = None
    start_base = None

    for i in range(start, total_len, 3):
        point = route['waypoints'][i]
        bike_bases = get_bike_bases_nearby(point['lat'], point['lng'], radius=600)
        if bike_bases:
            start_point_idx = i
            start_base = bike_bases[0]
            break
    
    if not start_base:
        return
    
    
    end_point_idx = None
    end_base = None

    for i in range(total_len-1, start_point_idx, -3):
        point = route['waypoints'][i]
        bike_bases = get_bike_bases_nearby(point['lat'], point['lng'], radius=600)
        if bike_bases:
            for bike_base in bike_bases:
                if bike_base["address"] != start_base["address"]:
                    end_point_idx = i
                    end_base = bike_base
                    break
            if end_base:
                break

    if not end_base:
        return

    return {
        'start': {'idx': start_point_idx,
                  'base': (start_base['lng'], start_base['lat'])},
        'end': {'idx': end_point_idx,
                'base': ( end_base['lng'], end_base['lat'])}
    }
