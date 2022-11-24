# completed
import mysql.connector

user = 'user1'
secret = 'user1'
session = False

try:
    session = mysql.connector.connect(
        host="localhost",
        user=user,
        password=secret,
        database='TestDB'
    )
    print("Connected!!!")
    cur = session.cursor()
    cur.execute("SELECT VERSION()")

    version = cur.fetchone()

    print("Database version: {}".format(version[0]))
except (Exception, mysql.connector.Error) as error:
    print("Something wrong: \n", error)
finally:
    if session:
        session.close()
        print("Session has closed")
