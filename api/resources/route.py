
from flask_restful import Resource, reqparse
from utils.make_routes import make_routes_with_water_transport


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
            return {'error': 'invalid coordinates'}, 400
            
        routes = make_routes_with_water_transport(args['from'], args['to'], args['vehicle'])

        return routes, 200