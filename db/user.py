from . import connect
import json
import psycopg2.extras

def insert(obj):
    db = connect.connectdb()
    c = db.cursor()
    c.execute("""INSERT INTO users (hash, username, created_at, description, password)
              VALUES (%s, %s, %s, %s, %s);""", (obj["hash"], obj["username"], obj["created_at"], obj["description"], obj["password"]))
    db.commit()
    db.close()


def select_by_timestamp(start, end):
    db = connect.connectdb()
    c = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * FROM users WHERE created_at >= (%s) AND created_at <= (%s) ORDER BY created_at;", (start, end))
    ret = c.fetchall()
    db.close()
    return ret

def query(target, value):
    db = connect.connectdb()
    c = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT * FROM users WHERE """ + target + """= (%s);""", (value, ))
    ret = c.fetchall()
    db.close()
    if len(ret) == 0:
        return None;
    return ret;
