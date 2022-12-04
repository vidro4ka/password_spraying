import psycopg2
from psycopg2 import Error

host = "localhost"
user = 'postgres'
secret = 'mypassword'
session = False

try:
    session = psycopg2.connect(user=user,
                               password=secret,
                               host=host,
                               dbname='testdb')
    cursor = session.cursor()
    print("Some info about PostgreSQL: \n", session.get_dsn_parameters(), "\n")
except (Exception, Error) as error:
    print("Error with PostgreSQL: ", error)
finally:
    if session:
        cursor.close()
        session.close()
        print("Connection with PostgreSQL has closed")
