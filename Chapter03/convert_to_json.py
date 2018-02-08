import json
from get_planet_data import get_planet_data
planets=get_planet_data()
json.dumps(planets)