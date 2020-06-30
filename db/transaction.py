from . import connect
import json
import psycopg2.extras

def insert(obj):
    db = connect.connectdb()
    c = db.cursor()
    c.execute("""INSERT INTO transactions (hash, sender, receiver, description, timestamp)
              VALUES (%s, %s, %s, %s, %s);""", (obj["hash"], obj["sender"], obj["receiver"], obj["description"], obj["timestamp"]))
    db.commit()
    db.close()


def select_by_timestamp(start, end):
    db = connect.connectdb()
    c = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * FROM transactions WHERE timestamp >= (%s) AND timestamp <= (%s);", (start, end))
    ret = c.fetchall()
    db.close()
    return ret
