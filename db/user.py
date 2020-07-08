from . import connect
import json
import psycopg2.extras

def insert(obj, c=None):
    db = None if c else connect.connectdb()
    if c == None:
        c = db.cursor()
    c.execute("""INSERT INTO users (hash, username, created_at, description, password)
              VALUES (%s, %s, %s, %s, %s);""", (obj["hash"], obj["username"], obj["created_at"], obj["description"], obj["api_key"]))
    if db:
        db.commit()
        db.close()


def select_by_timestamp(start, end, c=None):
    db = None if c else connect.connectdb()
    if c == None:
        c = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * FROM users WHERE created_at >= (%s) AND created_at <= (%s) ORDER BY created_at;", (start, end))
    ret = c.fetchall()
    if db:
        db.close()
    return ret

def query(target, value):
    db = connect.connectdb()
    c = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * FROM users WHERE " + target + "= (%s);", (value, ))
    ret = c.fetchall()
    db.close()
    if len(ret) == 0:
        return None;
    return ret;

def select_by_username(username, c=None):
    db = None if c else connect.connectdb()
    if c == None:
        c = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * FROM users WHERE username = (%s);", (username,))
    ret = c.fetchone()
    if db:
        db.close()
    return ret

def select_by_hash(hash, c=None):
    db = None if c else connect.connectdb()
    if c == None:
        c = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * FROM users WHERE hash = (%s);", (hash,))
    ret = c.fetchone()
    if db:
        db.close()
    return ret

def select_by_layer(layer, c=None):
    db = None if c else connect.connectdb()
    if c == None:
        c = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * FROM users WHERE layer = (%s);", (layer,))
    ret = c.fetchall()
    if db:
        db.close()
    return ret

>>>>>>> Migrate to database for did
