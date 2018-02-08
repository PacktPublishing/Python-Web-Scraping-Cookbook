import psycopg2

try:
	conn = psycopg2.connect("dbname='scraping' host='localhost' user='postgres' password='mypassword'")

	cur = conn.cursor()
	cur.execute('SELECT * from public."Planets"')
	rows = cur.fetchall()
	print(rows)

	cur.close()
	conn.close()

except Exception as ex:
	print(ex)
