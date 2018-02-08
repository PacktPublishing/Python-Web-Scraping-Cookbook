from elasticsearch import Elasticsearch
from get_planet_data import get_planet_data

# create an elastic search object
es = Elasticsearch()

# get the data
planet_data = get_planet_data()

for planet in planet_data:
	# insert each planet into elasticsearch server
	res = es.index(index='planets', doc_type='planets_info', body=planet)
	print (res)