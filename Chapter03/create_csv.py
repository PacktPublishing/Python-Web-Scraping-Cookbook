import csv
from get_planet_data import get_planet_data

planets = get_planet_data()

with open('../../www/planets.csv', 'w+') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(('Name', 'Mass', 'Radius', 'Description', 'MoreInfo'))
    for planet in planets:
        writer.writerow([planet['Name'], planet['Mass'],
        planet['Radius'], planet['Description'],
        planet['MoreInfo']])