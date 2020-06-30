import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

def connectdb(dbname="scoin"):
    try:
        db = psycopg2.connect(database="scoin", user=USERNAME, password=PASSWORD, host=HOST, port=PORT)
        return db
    except psycopg2.OperationalError as e:
        print("Error connecting database: %s" % (e))

