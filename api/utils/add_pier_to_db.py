import json

from loguru import logger

from src.db import session_maker
from src.pier import Pier


def add_pier_base_to_db():
    with open('init_files/piers.json', 'r') as file:
        piers_base_data = json.load(file)
    for data in piers_base_data:
        with session_maker() as session:
            pier = Pier(
                lat=data['pos']['Lat'],
                lng=data['pos']['Lon'],
            )
            session.add(pier)
            session.commit()
    logger.info(f'add_pier_base_to_db ok, len - {len(piers_base_data)}')

