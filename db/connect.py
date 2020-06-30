import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

def connectdb(dbname="scoin"):
    try:
        db = psycopg2.connect(database="scoin", user=USERNAME, password=PASSWORD, host=HOST, port=PORT)
        return db
    except psycopg2.OperationalError as e:
        print("Error connecting database: %s" % (e))

