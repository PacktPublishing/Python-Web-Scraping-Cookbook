import mysql.connector
import get_planet_data
from mysql.connector import errorcode
from get_planet_data import get_planet_data

try:
    # open the database connection
    cnx = mysql.connector.connect(user='root', password='mypassword',
                                  host="127.0.0.1", database="scraping")

    insert_sql = ("INSERT INTO Planets (Name, Mass, Radius, Description) " +
                  "VALUES (%(Name)s, %(Mass)s, %(Radius)s, %(Description)s)")

    # get the planet data
    planet_data = get_planet_data()

    # loop through all planets executing INSERT for each with the cursor
    cursor = cnx.cursor()
    for planet in planet_data:
        print("Storing data for %s" % (planet["Name"]))
        cursor.execute(insert_sql, planet)

    # commit the new records
    cnx.commit()

    # close the cursor and connection
    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
