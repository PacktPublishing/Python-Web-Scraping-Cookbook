import psycopg2
from get_planet_data import get_planet_data

try:
	# connect to PostgreSQL
	conn = psycopg2.connect("dbname='scraping' host='localhost' user='postgres' password='mypassword'")

	# the SQL INSERT statement we will use
	insert_sql = ('INSERT INTO public."Planets"(name, mass, radius, description, moreinfo) ' +
				  'VALUES (%(Name)s, %(Mass)s, %(Radius)s, %(Description)s, %(MoreInfo)s);')

	# open a cursor to access data
	cur = conn.cursor()

	# get the planets data and loop through each
	planet_data = get_planet_data()
	for planet in planet_data:
		# write each record
		cur.execute(insert_sql, planet)

	# commit the new records to the database
	conn.commit()
	cur.close()
	conn.close()

	print("Successfully wrote data to the database")

except Exception as ex:
	print(ex)
