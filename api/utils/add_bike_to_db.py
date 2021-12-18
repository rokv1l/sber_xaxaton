import json

from loguru import logger

from src.db import session_maker
from src.bike_base import BikeBase


def add_bike_base_to_db():
    with open('init_files/bike_new.json', 'r') as file:
        bike_base_data = json.load(file)
    for data in bike_base_data:
        with session_maker() as session:
            bike = BikeBase(
                address=data['addres'],
                lat=data['pos']['Lat'],
                lng=data['pos']['Lon'],
                is_open=True
            )
            session.add(bike)
            session.commit()
    logger.info(f'add_bike_base_to_db ok, len - {len(bike_base_data)}')

