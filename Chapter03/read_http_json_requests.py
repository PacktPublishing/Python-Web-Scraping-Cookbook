import requests
import json

planets_request = requests.get("http://localhost:8080/data/planets.json")
print(json.loads(planets_request.text))