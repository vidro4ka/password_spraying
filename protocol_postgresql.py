import psycopg2
from psycopg2 import Error

host = ""
user = ''
secret = ''
session = False

try:
    session = psycopg2.connect(user=user,
                               password=secret,
                               host=host,
                               dbname='TestDB')
    cursor = session.cursor()
    print("Some info about PostgreSQL: ", session.get_dsn_parameters(), "\n")
except (Exception, Error) as error:
    print("Error with PostgreSQL: ", error)
finally:
    if session:
        cursor.close()
        session.close()
        print("Connection with PostgreSQL has closed")
