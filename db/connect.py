from flask import g
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

def wrapper(f, *args):
    db = g.get("db", connectdb())
    c = g.get("cursor", db.cursor(cursor_factory=psycopg2.extras.RealDictCursor))
    ret = f(*args, c)
    if "db" not in g:
        db.commit()
        db.close()
    return ret

def start_commit():
    db = connectdb()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    g.db = db
    g.cursor = cursor

def end_commit():
    db = g.pop("db", None)
    g.pop("cursor", None)
    db.commit()
    db.close()

def close():
    db = g.pop("db", None)
    g.pop("cursor", None)
    if db:
        db.close()
