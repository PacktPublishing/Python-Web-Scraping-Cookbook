import requests
import csv

planets_request = requests.get("http://localhost:8080/data/planets.csv")

csv_data = planets_request.text.split("\n")

reader = csv.reader(csv_data, delimiter=',', quotechar='"')
for row in reader:
   print (row)