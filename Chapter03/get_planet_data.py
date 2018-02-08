from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_planet_data():
	html = urlopen("http://localhost:8080/planets.html")
	bsobj = BeautifulSoup(html, "lxml")

	planets = []
	planet_rows = bsobj.html.body.div.table.findAll("tr", {"class": "planet"})

	for i in planet_rows:
		tds = i.findAll("td")
		planet_data = dict()
		planet_data['Name'] = tds[1].text.strip()
		planet_data['Mass'] = tds[2].text.strip()
		planet_data['Radius'] = tds[3].text.strip()
		planet_data['Description'] = tds[4].text.strip()
		planet_data['MoreInfo'] = tds[5].findAll("a")[0]["href"].strip()
		planets.append(planet_data)

	return planets

if __name__ == "__main__":
	print(get_planet_data())
