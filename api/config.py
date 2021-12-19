
import os

db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')
db_username = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')

gh_url = os.getenv('GRAPHHOPPER_URL')

lenth_from_pier_limit = 30

FOOT_COLOR = '#A0E720'
SHIP_COLOR = '#4169E1'
BIKE_COLOR = '#00ADEE'