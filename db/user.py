from .connect import wrapper
import json
import psycopg2.extras

def insert(obj, c=None):
    def f(obj, c):
        c.execute("""INSERT INTO users (hash, username, created_at, description, api_key,
                  layer, public_key, private_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                  (obj["hash"], obj["username"], obj["created_at"], obj["description"],
                  obj["api_key"], obj["layer"], obj["public_key"], obj["private_key"]))
    wrapper(f, c, obj)


def select_by_timestamp(start, end, c=None):
    def f(start, end, c):
        c.execute("SELECT * FROM users WHERE created_at >= (%s) AND created_at <= (%s) ORDER BY created_at;", (start, end))
        return c.fetchall()
    return wrapper(f, c, start, end)

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
    return wrapper(f, c, username)

def select_by_hash(hash, c=None):
    def f(hash, c):
        c.execute("SELECT * FROM users WHERE hash = (%s);", (hash,))
        return c.fetchone()
    return wrapper(f, c, hash)

def select_by_layer(layer, c=None):
    def f(layer, c):
        c.execute("SELECT * FROM users WHERE layer = (%s);", (layer,))
        return c.fetchall()
    return wrapper(f, c, layer)

def get_user_amount(c=None):
    def f(c):
        c.execute("SELECT count(*) FROM users;")
        return c.fetchone()["count"]
    return wrapper(f, c)

def set_layer_by_username(username, layer, c=None):
    def f(username, layer, c):
        c.execute("UPDATE users SET layer = (%s) WHERE username = (%s);", (layer, username))
    wrapper(f, c, username, layer)
