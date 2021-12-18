
from copy import deepcopy
from flask_restful import Resource, reqparse
from utils.graphhopper import get_route
from utils.multi_modal import enrich_foot_route


class Route(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', required=True)
        parser.add_argument('to', required=True)
        parser.add_argument('vehicle', default='foot')
        
        args = parser.parse_args() 
        try:
            args['from'] = list(map(float, args['from'].split(',')))
            args['to'] = list(map(float, args['to'].split(',')))
        except:
            return {'error': 'invalid coordinates'}, 404
            
        routes = []

        route = get_route([args['from'], args['to']], args['vehicle'])
        route['points'] = []
                    
        if args['vehicle'] == 'foot' and route["dist"] > 2000:
            multi_route = enrich_foot_route(deepcopy(route))
            if multi_route:
                routes.append(multi_route)
        
        route["waypoints"] = [{ "waypoint" : route["waypoints"], "color" : "#62cc00"}]
        routes.append(route)

        return routes, 200