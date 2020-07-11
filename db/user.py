from .connect import wrapper
import json
import psycopg2.extras

def insert(obj, c=None):
    def f(obj, c):
        c.execute("""INSERT INTO users (hash, username, created_at, description, api_key,
                  layer, public_key, private_ke) VALUES (%s, %s, %s, %s, %s);""",
                  (obj["hash"], obj["username"], obj["created_at"], obj["description"],
                  obj["api_key"], obj["layer"], obj["public_key"], obj["private_key"]))
    wrapper(f, obj)()


def select_by_timestamp(start, end, c=None):
    def f(start, end, c):
        c.execute("SELECT * FROM users WHERE created_at >= (%s) AND created_at <= (%s) ORDER BY created_at;", (start, end))
        return c.fetchall()
    return wrapper(f, start, end)()

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
    def f(username, c):
        c.execute("SELECT * FROM users WHERE username = (%s);", (username,))
        return c.fetchone()
    return wrapper(f, username)()

def select_by_hash(hash, c=None):
    def f(hash, c):
        c.execute("SELECT * FROM users WHERE hash = (%s);", (hash,))
        return c.fetchone()
    return wrapper(f, hash)()

def select_by_layer(layer, c=None):
    def f(layer, c):
        c.execute("SELECT * FROM users WHERE layer = (%s);", (layer,))
        return c.fetchall()
    return wrapper(f, layer)()
