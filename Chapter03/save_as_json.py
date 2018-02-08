import json
from get_planet_data import get_planet_data
planets=get_planet_data()
with open('../../data/planets.json', 'w+') as jsonFile:
	json.dump(planets, jsonFile, indent=4)