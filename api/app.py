from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from src.db import session_maker
from src.bike_base import BikeBase
from src.pier import Pier
from utils.add_bike_to_db import add_bike_base_to_db
from utils.add_pier_to_db import add_pier_base_to_db
from resources.hello import Hello
from resources.route import Route


app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Hello, '/hello')
api.add_resource(Route, '/route')


if __name__ == '__main__':
    with session_maker() as session:
        bikes = session.query(BikeBase).count()
        if not bikes:
            add_bike_base_to_db()
        piers = session.query(Pier).count()
        if not piers:
            add_pier_base_to_db()

    app.run(host='0.0.0.0', port=5000, debug=True)